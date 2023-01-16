from django.db import models


class Login(models.Model):
    username = models.CharField(max_length=200, primary_key=True, error_messages={"unique": "Already Existing"})
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.username


class Register(models.Model):
    Full_Name = models.CharField(max_length=100)
    username = models.CharField(max_length=200, primary_key=True, error_messages={"unique": "Already Existing"})
    password = models.CharField(max_length=200)
    contact = models.CharField(max_length=15)
    Gender = models.CharField(max_length=10)
    Email = models.CharField(max_length=50)
    Account_type = models.CharField(max_length=10)

    def __str__(self):
        return self.username


class Logo_listing(models.Model):
    YES = '1'
    NO = '0'
    SELECTED_CHOICE = [
        (YES, 'yes'),
        (NO, 'no')]
    Title = models.CharField(max_length=100, primary_key=True, error_messages={"unique": "Already Existing"})
    Description = models.TextField()
    Creator = models.CharField(max_length=200, default="admin")
    Status = models.CharField(max_length=2, choices=SELECTED_CHOICE, default=NO)
    Owner = models.CharField(max_length=200)
    Image = models.ImageField(upload_to="auction_images")

    def __str__(self):
        return self.Title


class Logo_Bid_details(models.Model): #to be deleted after every win
    YES = '1'
    NO = '0'
    SELECTED_CHOICE = [
        (YES, 'yes'),
        (NO, 'no')]
    Title = models.CharField(max_length=100, primary_key=True, error_messages={"unique": "Already Existing"})
    AuctionStart = models.DateTimeField()
    AuctionEnd = models.DateTimeField()
    StartBidAmount = models.IntegerField(default=100)
    WinStatus = models.CharField(max_length=2, choices=SELECTED_CHOICE, default=NO)

    def __str__(self):
        return self.Title

class Bids(models.Model):
    Title = models.CharField(max_length=100) #can be foreign key
    Bidder = models.CharField(max_length=200)
    Amount = models.IntegerField()

    def __str__(self):
        return self.Title




