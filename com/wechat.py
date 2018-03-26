import re
import time

import itchat
from pandas import DataFrame

import log
import syscall


class WeChat(object):
    def __init__(self, debug=False, blockThread=False):
        self.debug = debug
        self.blockThread = blockThread

        self.instance = itchat.new_instance()

        self.instance.auto_login(hotReload=True)

        for i in self.instance.get_mps(update=True):
            if '小冰' == i.get('NickName'):
                self.xiaobing = i.get('UserName')

        self.friends = self.instance.get_friends()

        self.redirect = {'state': 0, 'user': None}
        self.history = []

        @self.instance.msg_register(itchat.content.INCOME_MSG, isFriendChat=True)
        def onReceive(msg):
            if self.is_command(msg):
                return

            self.dump_msg(msg)

            user = msg.user.get('RemarkName') or msg.user.get(
                'NickName') or msg.user.get('UserName')

            if 1 == self.redirect['state'] and self.redirect['user'] == user:
                self._req = msg.user.get('UserName')
                self.instance.send(msg.content, toUserName=self.xiaobing)

        @self.instance.msg_register(itchat.content.INCOME_MSG, isMpChat=True)
        def onReply(msg):
            self.dump_msg(msg)
            if 1 == self.redirect['state']:
                self.instance.send(msg.content, toUserName=self._req)

    def run(self):
        self.instance.run(blockThread=self.blockThread, debug=self.debug)

    def dump_msg(self, msg):
        if msg.Type == itchat.content.TEXT:
            user = msg.user.get('RemarkName') or msg.user.get(
                'NickName') or msg.user.get('UserName')
            print("[%s] %s\n    %s" %
                  (time.strftime("%Y/%m/%d %H:%M:%S"), user,  msg.Text))

    def is_command(self, msg):
        if 'filehelper' == msg.ToUserName and msg.Type == itchat.content.TEXT:
            r = re.split('//', msg.Text)
            if len(r) == 2:
                self.redirect['state'] = int(r[0])
                self.redirect['user'] = r[1]

                print("redirect state %d, user %s" %
                      (self.redirect['state'], self.redirect['user']))

                self.history.append("redirect state %d, user %s" % (
                    self.redirect['state'], self.redirect['user']))
                DataFrame({'history': self.history}).to_csv('._history.csv')
                return True
        return False


if __name__ == '__main__':
    obj = WeChat(debug=True, blockThread=True)
    obj.run()
