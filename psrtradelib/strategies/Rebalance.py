import backtrader as bt


class Rebalance(bt.Strategy):
    params = (('assets', list()),
              ('rebalance_months', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]))  # Float: 1 == 100%

    def __init__(self):
        self.rebalance_dict = dict()
        self.month = 0
        for i, d in enumerate(self.datas):
            self.rebalance_dict[d] = dict()
            self.rebalance_dict[d]['rebalanced'] = False
            for asset in self.p.assets:
                if asset[0] == d._name:
                    self.rebalance_dict[d]['target_percent'] = asset[1]

    def prenext(self):
        self.next()

    def next(self):
        for i, d in enumerate(self.datas):
            dt = d.datetime.datetime()
            dn = d._name
            pos = self.getposition(d).size
            if dt.month is not self.month:
                # and self.rebalance_dict[d]['rebalanced'] is False:
                print('{}: Sending Order: {} | Month {} | Rebalanced: {} | Pos: {}'.format(dt, dn, dt.month,
                                                                                          self.rebalance_dict[d][
                                                                                              'rebalanced'], pos))
                self.order_target_percent(d, target=self.rebalance_dict[d]['target_percent'] / 100)
                # self.rebalance_dict[d]['rebalanced'] = True
                self.month = dt.month

            # # Reset
            # if dt.month not in self.p.rebalance_months:
            #     self.rebalance_dict[d]['rebalanced'] = False

    def notify_order(self, order):
        date = self.data.datetime.datetime().date()

        if order.status == order.Completed:
            print('{} >> Order Completed >> Stock: {},  Ref: {}, Size: {}, Price: {}'.format(

                date,
                order.data._name,
                order.ref,
                order.size,
                'NA' if not order.price else round(order.price, 5)
            ))

    def notify_trade(self, trade):
        date = self.data.datetime.datetime().date()
        if trade.isclosed:
            print('{} >> Notify Trade >> Stock: {}, Close Price: {}, Profit, Gross {}, Net {}'.format(
                date,
                trade.data._name,
                trade.price,
                round(trade.pnl, 2),
                round(trade.pnlcomm, 2)))
