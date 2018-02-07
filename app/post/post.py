from app.post import post
from util.sendMail import send_mail


###########################################
#                                         #
#          Non-Authorized Code            #
#                                         #
###########################################

@post.route('/sendmail', methods=['GET', 'POST'])
def sendmail():
    send_mail("hi", ["mk5986@nyu.edu"], "hello")
    return "Sent."

