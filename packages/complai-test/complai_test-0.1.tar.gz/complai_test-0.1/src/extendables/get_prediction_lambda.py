import logging

class NiceLambda():
    def __init__(self):
        logging.info("In Dummy Lambda Constructor")

    def pred_lambda(self,x,**kwargs):
        return True