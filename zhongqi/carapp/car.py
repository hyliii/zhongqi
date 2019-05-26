from modelapp.models import Book


class Cartltem():
    def __init__(self,book,amount):
        self.amount=amount
        self.book=book
        self.status=1
class Cart():
    def __init__(self):
        self.sum_price=0
        self.total_price=0
        self.p_price = 0
        self.cartltems=[]
        self.dustbin=[]
        self.sum_amount = 0
    def c_sums(self):
        self.sum_amount=0
        self.sum_price=0
        self.total_price=0
        for i in self.cartltems:
            self.sum_amount += i.amount
            self.p_price=i.book.price*int(i.amount)
            self.sum_price+=i.book.price*int(i.amount)
            self.total_price+=(i.book.ddprice-i.book.price)*int(i.amount)
    def c_add(self,b_id,amount):
        for i in self.cartltems:
            if int(i.book.id)==int(b_id):
                i.amount+=int(amount)
                self.c_sums()
                return
        else:
            book=Book.objects.filter(id=b_id)[0]
            self.cartltems.append(Cartltem(book,amount))
            self.c_sums()
    def c_update(self,b_id,amount):
        for i in self.cartltems:
            if int(i.book.id)==int(b_id):
                i.amount=int(amount)
        self.c_sums()
    def c_remove(self,b_id,order,amount):
        for i in self.cartltems:
            if i.book.id==int(b_id) :
                if order=='1':
                    self.cartltems.remove(i)
                else:
                    for j in self.dustbin:
                        if int(j.book.id) == int(b_id):
                            j.amount += int(amount)
                            self.cartltems.remove(i)
                            return
                    else:
                        self.dustbin.append(i)
                        self.cartltems.remove(i)
                        return
    def c_recover(self,b_id,order,amount):
        for i in self.dustbin:
            if i.book.id==int(b_id) :
                if order=='3':
                    self.dustbin.remove(i)
                else:
                    for j in self.cartltems:
                        if int(j.book.id) == int(b_id):
                            j.amount += int(amount)
                            self.dustbin.remove(i)
                            return
                    else:
                        self.cartltems.append(i)
                        self.dustbin.remove(i)
                        return


