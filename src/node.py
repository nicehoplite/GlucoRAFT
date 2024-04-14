import threading
import time
import utils as utils
from config import cfg

FOLLOWER = 0
CANDIDATE = 1
LEADER = 2


class Node():
    def __init__(self, fellow, my_ip):
        self.addr = my_ip
        self.fellow = fellow
        self.lock = threading.Lock()
        self.DB = {}
        self.log = []
        self.staged = None
        self.term = 0
        self.status = FOLLOWER
        self.majority = ((len(self.fellow) + 1) // 2) + 1
        self.voteCount = 0
        self.commitIdx = 0
        self.timeout_thread = None
        self.init_timeout()

    def incrementVote(self):
        self.voteCount += 1
        if self.voteCount >= self.majority:
            print(f"Current Leader:{self.addr}  Current Term:{self.term}")
            self.status = LEADER
            self.startHeartBeat()

    def startElection(self):
        self.term += 1
        self.voteCount = 0
        self.status = CANDIDATE
        self.init_timeout()
        self.incrementVote()
        self.send_vote_req()

    def send_vote_req(self):
        for voter in self.fellow:
            threading.Thread(target=self.ask_for_vote,
                             args=(voter, self.term)).start()


    def ask_for_vote(self, voter, term):
        message = {
            "term": term,
            "commitIdx": self.commitIdx,
            "staged": self.staged
        }
        route = "vote_req"
        while self.status == CANDIDATE and self.term == term:
            reply = utils.send(voter, route, message)
            if reply:
                choice = reply.json()["choice"]
                if choice and self.status == CANDIDATE:
                    self.incrementVote()
                elif not choice:
                    term = reply.json()["term"]
                    if term > self.term:
                        self.term = term
                        self.status = FOLLOWER
                break

    def decide_vote(self, term, commitIdx, staged):
        if self.term < term and self.commitIdx <= commitIdx and (
                staged or (self.staged == staged)):
            self.reset_timeout()
            self.term = term
            return True, self.term
        else:
            return False, self.term

    def startHeartBeat(self):
        print("Sending out Heartbeat")
        if self.staged:
            self.handle_put(self.staged)

        for each in self.fellow:
            t = threading.Thread(target=self.send_heartbeat, args=(each, ))
            t.start()

    def update_follower_commitIdx(self, follower):
        route = "heartbeat"
        first_message = {"term": self.term, "addr": self.addr}
        second_message = {
            "term": self.term,
            "addr": self.addr,
            "action": "commit",
            "payload": self.log[-1]
        }
        reply = utils.send(follower, route, first_message)
        if reply and reply.json()["commitIdx"] < self.commitIdx:
            reply = utils.send(follower, route, second_message)

    def send_heartbeat(self, follower):
        if self.log:
            self.update_follower_commitIdx(follower)

        route = "heartbeat"
        message = {"term": self.term, "addr": self.addr}
        while self.status == LEADER:
            start = time.time()
            reply = utils.send(follower, route, message)
            if reply:
                self.heartbeat_reply_handler(reply.json()["term"],
                                             reply.json()["commitIdx"])
            delta = time.time() - start
            time.sleep((cfg.HB_TIME - delta) / 1000)

    def heartbeat_reply_handler(self, term, commitIdx):
        if term > self.term:
            self.term = term
            self.status = FOLLOWER
            self.init_timeout()


    def reset_timeout(self):
        self.election_time = time.time() + utils.random_timeout()

    # /heartbeat

    def heartbeat_follower(self, msg):
        term = msg["term"]
        if self.term <= term:
            self.leader = msg["addr"]
            self.reset_timeout()

            if self.status == CANDIDATE:
                self.status = FOLLOWER
            elif self.status == LEADER:
                self.status = FOLLOWER
                self.init_timeout()
  
            if self.term < term:
                self.term = term

            if "action" in msg:
                print("received action", msg)
                action = msg["action"]
                # logging after first msg
                if action == "log":
                    payload = msg["payload"]
                    self.staged = payload
                # proceeding staged transaction
                elif self.commitIdx <= msg["commitIdx"]:
                    if not self.staged:
                        self.staged = msg["payload"]
                    self.commit()

        return self.term, self.commitIdx

    # initiate timeout thread, or reset it
    def init_timeout(self):
        self.reset_timeout()
        if self.timeout_thread and self.timeout_thread.is_alive():
            return
        self.timeout_thread = threading.Thread(target=self.timeout_loop)
        self.timeout_thread.start()

    def timeout_loop(self):
        while self.status != LEADER:
            delta = self.election_time - time.time()
            if delta < 0:
                self.startElection()
            else:
                time.sleep(delta)

    def handle_get(self, payload):
        print("getting", payload)
        key = payload["key"]
        if key in self.DB:
            payload["value"] = self.DB[key]
            return payload
        else:
            return None

    def spread_update(self, message, confirmations=None, lock=None):
        for i, each in enumerate(self.fellow):
            r = utils.send(each, "heartbeat", message)
            if r and confirmations:
                confirmations[i] = True
        if lock:
            lock.release()

    def handle_put(self, payload):
        print("putting", payload)


        self.lock.acquire()
        self.staged = payload
        waited = 0
        log_message = {
            "term": self.term,
            "addr": self.addr,
            "payload": payload,
            "action": "log",
            "commitIdx": self.commitIdx
        }


        log_confirmations = [False] * len(self.fellow)
        threading.Thread(target=self.spread_update,
                         args=(log_message, log_confirmations)).start()
        while sum(log_confirmations) + 1 < self.majority:
            waited += 0.0005
            time.sleep(0.0005)
            if waited > cfg.MAX_LOG_WAIT / 1000:
                print(f"waited {cfg.MAX_LOG_WAIT} ms, update rejected:")
                self.lock.release()
                return False

        commit_message = {
            "term": self.term,
            "addr": self.addr,
            "payload": payload,
            "action": "commit",
            "commitIdx": self.commitIdx
        }
        self.commit()
        threading.Thread(target=self.spread_update,
                         args=(commit_message, None, self.lock)).start()
        print("majority reached, replied to client, sending message to commit")
        return True

    def commit(self):
        self.commitIdx += 1
        self.log.append(self.staged)
        key = self.staged["key"]
        value = self.staged["value"]
        self.DB[key] = value
        self.staged = None
