from django.db import models


class Player(models.Model):
    POSITION_CHOICES = (
        ("P", "Pitcher"),
        ("C", "Catcher"),
        ("1B", "First Base"),
        ("2B", "Second Base"),
        ("3B", "Third Base"),
        ("SS", "Shortstop"),
        ("LF", "Left Field"),
        ("CF", "Center Field"),
        ("RF", "Right Field"),
        ("DH", "Designated Hitter")
    )
    fName = models.CharField(max_length=50, verbose_name="First Name")
    lName = models.CharField(max_length=50, verbose_name="Last Name")
    position = models.CharField(max_length=2,
                                choices=POSITION_CHOICES,
                                blank=True,
                                null=True)

    def __str__(self):
        return self.fName + " " + self.lName


class Statistics(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField()
    G = models.PositiveSmallIntegerField(verbose_name="Games Played",
                                         blank=True,
                                         null=True)
    PA = models.PositiveSmallIntegerField(verbose_name="Plate Appearances",
                                          blank=True,
                                          null=True)
    HR = models.PositiveSmallIntegerField(verbose_name="Home Runs",
                                          blank=True,
                                          null=True)
    R = models.PositiveSmallIntegerField(verbose_name="Runs Scored",
                                         blank=True,
                                         null=True)
    RBI = models.PositiveSmallIntegerField(verbose_name="Runs Batted In",
                                           blank=True,
                                           null=True)
    BB = models.PositiveSmallIntegerField(verbose_name="Walks",
                                          blank=True,
                                          null=True)
    IBB = models.PositiveSmallIntegerField(verbose_name="Intentional Walks",
                                           blank=True,
                                           null=True)
    SO = models.PositiveSmallIntegerField(verbose_name="Strike Outs",
                                          blank=True,
                                          null=True)
    HBP = models.PositiveSmallIntegerField(verbose_name="Hits By Pitch",
                                           blank=True,
                                           null=True)
    SF = models.PositiveSmallIntegerField(verbose_name="Sacrifice Flies",
                                          blank=True,
                                          null=True)
    SH = models.PositiveSmallIntegerField(verbose_name="Sacrifice Hits",
                                          blank=True,
                                          null=True)
    GDP = models.PositiveSmallIntegerField(verbose_name="Grounded into Double Plays",
                                           blank=True,
                                           null=True)
    SB = models.PositiveSmallIntegerField(verbose_name="Stolen Bases",
                                          blank=True,
                                          null=True)
    CS = models.PositiveSmallIntegerField(verbose_name="Caught Stealing",
                                          blank=True,
                                          null=True)
    AVG = models.FloatField(verbose_name="Batting Average",
                            blank=True,
                            null=True)
    OBP = models.FloatField(verbose_name="On-Base Percentage",
                            blank=True,
                            null=True)
    SLG = models.FloatField(verbose_name="Slugging Percentage",
                            blank=True,
                            null=True)
    OPS = models.FloatField(verbose_name="On-Base Plus Slugging",
                            blank=True,
                            null=True)
    fAVG = models.FloatField(verbose_name="Fantasy Batting Average",
                                            blank=True,
                                            null=True)
    fOPS = models.PositiveSmallIntegerField(verbose_name="Fantasy On-Base Plus Slugging",
                                            blank=True,
                                            null=True)
    fHR = models.PositiveSmallIntegerField(verbose_name="Fantasy Home Runs",
                                           blank=True,
                                           null=True)
    fRBI = models.PositiveSmallIntegerField(verbose_name="Fantasy Runs Batted In",
                                            blank=True,
                                            null=True)
    fR = models.PositiveSmallIntegerField(verbose_name="Fantasy Runs Scored",
                                          blank=True,
                                          null=True)
    fSB = models.PositiveSmallIntegerField(verbose_name="Fantasy Stolen Bases",
                                           blank=True,
                                           null=True)

    class Meta:
        verbose_name_plural = 'Statistics'
        ordering = ('id',)

    def get_field_names(self):
        name_list = []
        for field in self._meta.fields:
            name_list.append({'name': field.name,
                              'value': getattr(self, field.name)})
        return name_list
