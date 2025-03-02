class BStopByLoss:
    def __init__(self, rounds, delta=0.01):
        '''
        连续rounds次, train_loss - min_train_loss > delta, 则停止训练
        '''
        self.rounds = rounds
        self.delta = delta
        self.min_trainLoss = float('inf')
        self.cnt = 0

        self.cnt_list = []
    def __call__(self, train_loss):
        if train_loss >= self.min_trainLoss + self.delta:
            self.cnt += 1
        elif train_loss < self.min_trainLoss:
            self.min_trainLoss = train_loss
            if self.cnt != 0:
                self.cnt -= 1

        self.cnt_list.append(self.cnt)
        if self.cnt > self.rounds:
            return True
        return False