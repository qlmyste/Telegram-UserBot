Skip to content
Search or jump to…

Pull requests
Issues
Marketplace
Explore
 
@PolisanTheEasyNick 
6
11137AvinashReddy3108/PaperplaneExtended
 Code Issues 7 Pull requests 0 Actions Projects 0 Wiki Security Insights
PaperplaneExtended/userbot/modules/sql_helper/filter_sql.py
@AvinashReddy3108 AvinashReddy3108 Goodbye PPEx [4th October 2019]
3d2b751 2 days ago
@baalajimaestro@AvinashReddy3108@SpEcHiDe@raphielscape@zakaryan2004@Prakasaka@Muttahir786@jaskaranSM@yshalsager@nitanmarcel@kandnub@shxnpie
71 lines (56 sloc)  1.88 KB
  
try:
    from userbot.modules.sql_helper import SESSION, BASE
except ImportError:
    raise AttributeError
from sqlalchemy import Column, UnicodeText, Numeric, String


class Filters(BASE):
    __tablename__ = "filters"
    chat_id = Column(String(14), primary_key=True)
    keyword = Column(UnicodeText, primary_key=True, nullable=False)
    reply = Column(UnicodeText)
    f_mesg_id = Column(Numeric)

    def __init__(self, chat_id, keyword, reply, f_mesg_id):
        self.chat_id = str(chat_id)
        self.keyword = keyword
        self.reply = reply
        self.f_mesg_id = f_mesg_id

    def __eq__(self, other):
        return bool(
            isinstance(other, Filters) and self.chat_id == other.chat_id
            and self.keyword == other.keyword)


Filters.__table__.create(checkfirst=True)


def get_filter(chat_id, keyword):
    try:
        return SESSION.query(Filters).get((str(chat_id), keyword))
    finally:
        SESSION.close()


def get_filters(chat_id):
    try:
        return SESSION.query(Filters).filter(
            Filters.chat_id == str(chat_id)).all()
    finally:
        SESSION.close()


def add_filter(chat_id, keyword, reply, f_mesg_id):
    to_check = get_filter(chat_id, keyword)
    if not to_check:
        adder = Filters(str(chat_id), keyword, reply, f_mesg_id)
        SESSION.add(adder)
        SESSION.commit()
        return True
    else:
        rem = SESSION.query(Filters).get((str(chat_id), keyword))
        SESSION.delete(rem)
        SESSION.commit()
        adder = Filters(str(chat_id), keyword, reply, f_mesg_id)
        SESSION.add(adder)
        SESSION.commit()
        return False


def remove_filter(chat_id, keyword):
    to_check = get_filter(chat_id, keyword)
    if not to_check:
        return False
    else:
        rem = SESSION.query(Filters).get((str(chat_id), keyword))
        SESSION.delete(rem)
        SESSION.commit()
        return True
© 2019 GitHub, Inc.
Terms
Privacy
Security
Status
Help
Contact GitHub
Pricing
API
Training
Blog
About
