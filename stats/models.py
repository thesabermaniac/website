from django.db import models
from fractions import Fraction as frac


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


class HittingStatistics(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField(verbose_name="Year")
    is_projection = models.BooleanField(default=False)
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
    fG = models.SmallIntegerField(verbose_name="Fantasy Games Played",
                                  blank=True,
                                  null=True)
    fPA = models.SmallIntegerField(verbose_name="Fantasy Plate Appearances",
                                   blank=True,
                                   null=True)
    fHR = models.SmallIntegerField(verbose_name="Fantasy Home Runs",
                                   blank=True,
                                   null=True)
    fR = models.SmallIntegerField(verbose_name="Fantasy Runs Scored",
                                  blank=True,
                                  null=True)
    fRBI = models.SmallIntegerField(verbose_name="Fantasy Runs Batted In",
                                    blank=True,
                                    null=True)
    fBB = models.SmallIntegerField(verbose_name="Fantasy Walks",
                                   blank=True,
                                   null=True)
    fIBB = models.SmallIntegerField(verbose_name="Fantasy Intentional Walks",
                                    blank=True,
                                    null=True)
    fSO = models.SmallIntegerField(verbose_name="Fantasy Strikeouts",
                                   blank=True,
                                   null=True)
    fHBP = models.SmallIntegerField(verbose_name="Fantasy Hit By Pitch",
                                    blank=True,
                                    null=True)
    fSF = models.SmallIntegerField(verbose_name="Fantasy Sacrifice Flies",
                                   blank=True,
                                   null=True)
    fSH = models.SmallIntegerField(verbose_name="Fantasy Sacrifice Hits",
                                   blank=True,
                                   null=True)
    fGDP = models.SmallIntegerField(verbose_name="Fantasy Grounded into Double Plays",
                                    blank=True,
                                    null=True)
    fSB = models.SmallIntegerField(verbose_name="Fantasy Stolen Bases",
                                   blank=True,
                                   null=True)
    fCS = models.SmallIntegerField(verbose_name="Fantasy Caught Stealing",
                                   blank=True,
                                   null=True)
    fAVG = models.SmallIntegerField(verbose_name="Fantasy Batting Average",
                                    blank=True,
                                    null=True)
    fOBP = models.SmallIntegerField(verbose_name="Fantasy On Base Percentage",
                                    blank=True,
                                    null=True)
    fSLG = models.SmallIntegerField(verbose_name="Fantasy Slugging Percentage",
                                    blank=True,
                                    null=True)
    fOPS = models.SmallIntegerField(verbose_name="Fantasy On-Base Plus Slugging",
                                    blank=True,
                                    null=True)
    fTotal = models.SmallIntegerField(verbose_name="Fantasy Total",
                                      blank=True,
                                      null=True)

    class Meta:
        verbose_name_plural = 'Hitting Statistics'
        ordering = ('fTotal', 'id')

    def get_field_names_and_values(self):
        name_list = []
        for field in self._meta.fields:
            name_list.append({'name': field.name,
                              'value': getattr(self, field.name)})
        return name_list

    def get_field_names(self):
        name_list = []
        for field in self._meta.fields:
            name_list.append(field.name)
        return name_list


class PitchingStatistics(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField(verbose_name="Year")
    is_projection = models.BooleanField(default=False)
    W = models.SmallIntegerField(verbose_name="Wins",
                                 blank=True,
                                 null=True,
                                 default=0)
    L = models.SmallIntegerField(verbose_name="Losses",
                                 blank=True,
                                 null=True,
                                 default=0)
    ERA = models.FloatField(verbose_name="Earned Run Average",
                            blank=True,
                            null=True,
                            default=0.0)
    WHIP = models.FloatField(verbose_name="Walks + Hits/IP",
                             blank=True,
                             null=True,
                             default=0.0)
    G = models.SmallIntegerField(verbose_name="Games Played",
                                 blank=True,
                                 null=True,
                                 default=0)
    GS = models.SmallIntegerField(verbose_name="Games Started",
                                  blank=True,
                                  null=True,
                                  default=0)
    CG = models.SmallIntegerField(verbose_name="Complete Games",
                                  blank=True,
                                  null=True,
                                  default=0)
    ShO = models.SmallIntegerField(verbose_name="Shutouts",
                                   blank=True,
                                   null=True,
                                   default=0)
    SV = models.SmallIntegerField(verbose_name="Saves",
                                  blank=True,
                                  null=True,
                                  default=0)
    HLD = models.SmallIntegerField(verbose_name="Holds",
                                   blank=True,
                                   null=True,
                                   default=0)
    BS = models.SmallIntegerField(verbose_name="Blown Saves",
                                  blank=True,
                                  null=True,
                                  default=0)
    IP = models.DecimalField(verbose_name="Innings Pitched",
                             decimal_places=1,
                             max_digits=5,
                             blank=True,
                             null=True,
                             default=0.0)
    TBF = models.SmallIntegerField(verbose_name="Total Batters Faced",
                                   blank=True,
                                   null=True,
                                   default=0)
    H = models.SmallIntegerField(verbose_name="Hits Allowed",
                                 blank=True,
                                 null=True,
                                 default=0)
    R = models.SmallIntegerField(verbose_name="Runs Allowed",
                                 blank=True,
                                 null=True,
                                 default=0)
    ER = models.SmallIntegerField(verbose_name="Earned Runs Allowed",
                                  blank=True,
                                  null=True,
                                  default=0)
    HR = models.SmallIntegerField(verbose_name="Home Runs Allowed",
                                  blank=True,
                                  null=True,
                                  default=0)
    BB = models.SmallIntegerField(verbose_name="Walks Allowed",
                                  blank=True,
                                  null=True,
                                  default=0)
    IBB = models.SmallIntegerField(verbose_name="Intentional Walks Allowed",
                                   blank=True,
                                   null=True,
                                   default=0)
    HBP = models.SmallIntegerField(verbose_name="Hits By Pitch",
                                   blank=True,
                                   null=True,
                                   default=0)
    WP = models.SmallIntegerField(verbose_name="Wild Pitches",
                                  blank=True,
                                  null=True,
                                  default=0)
    SO = models.SmallIntegerField(verbose_name="Strikeouts",
                                  blank=True,
                                  null=True,
                                  default=0)

    fW = models.SmallIntegerField(verbose_name="Fantasy Wins",
                                  blank=True,
                                  null=True,
                                  default=0)
    fL = models.SmallIntegerField(verbose_name="Fantasy Losses",
                                  blank=True,
                                  null=True,
                                  default=0)
    fERA = models.FloatField(verbose_name="Fantasy Earned Run Average",
                             blank=True,
                             null=True,
                             default=0.0)
    fWHIP = models.FloatField(verbose_name="Fantasy Walks + Hits/IP",
                              blank=True,
                              null=True,
                              default=0.0)
    fG = models.SmallIntegerField(verbose_name="Fantasy Games Played",
                                  blank=True,
                                  null=True,
                                  default=0)
    fGS = models.SmallIntegerField(verbose_name="Fantasy Games Started",
                                   blank=True,
                                   null=True,
                                   default=0)
    fCG = models.SmallIntegerField(verbose_name="Fantasy Complete Games",
                                   blank=True,
                                   null=True,
                                   default=0)
    fShO = models.SmallIntegerField(verbose_name="Fantasy Shutouts",
                                    blank=True,
                                    null=True,
                                    default=0)
    fSV = models.SmallIntegerField(verbose_name="Fantasy Saves",
                                   blank=True,
                                   null=True,
                                   default=0)
    fHLD = models.SmallIntegerField(verbose_name="Fantasy Holds",
                                    blank=True,
                                    null=True,
                                    default=0)
    fBS = models.SmallIntegerField(verbose_name="Fantasy Blown Saves",
                                   blank=True,
                                   null=True,
                                   default=0)
    fIP = models.FloatField(verbose_name="Fantasy Innings Pitched",
                            blank=True,
                            null=True,
                            default=0.0)
    fTBF = models.SmallIntegerField(verbose_name="Fantasy Total Batters Faced",
                                    blank=True,
                                    null=True,
                                    default=0)
    fH = models.SmallIntegerField(verbose_name="Fantasy Hits Allowed",
                                  blank=True,
                                  null=True,
                                  default=0)
    fR = models.SmallIntegerField(verbose_name="Fantasy Runs Allowed",
                                  blank=True,
                                  null=True,
                                  default=0)
    fER = models.SmallIntegerField(verbose_name="Fantasy Earned Runs Allowed",
                                   blank=True,
                                   null=True,
                                   default=0)
    fHR = models.SmallIntegerField(verbose_name="Fantasy Home Runs Allowed",
                                   blank=True,
                                   null=True,
                                   default=0)
    fBB = models.SmallIntegerField(verbose_name="Fantasy Walks Allowed",
                                   blank=True,
                                   null=True,
                                   default=0)
    fIBB = models.SmallIntegerField(verbose_name="Fantasy Intentional Walks Allowed",
                                    blank=True,
                                    null=True,
                                    default=0)
    fHBP = models.SmallIntegerField(verbose_name="Fantasy Hits By Pitch",
                                    blank=True,
                                    null=True,
                                    default=0)
    fWP = models.SmallIntegerField(verbose_name="Fantasy Wild Pitches",
                                   blank=True,
                                   null=True,
                                   default=0)
    fSO = models.SmallIntegerField(verbose_name="Fantasy Strikeouts",
                                   blank=True,
                                   null=True,
                                   default=0)
    fTotal = models.SmallIntegerField(verbose_name="Fantasy Total",
                                      blank=True,
                                      null=True,
                                      default=0)

    class Meta:
        verbose_name_plural = 'Pitching Statistics'
        ordering = ('fTotal', 'id')

    def get_field_names_and_values(self):
        name_list = []
        for field in self._meta.fields:
            name_list.append({'name': field.name,
                              'value': getattr(self, field.name)})
        return name_list

    def get_field_names(self):
        name_list = []
        for field in self._meta.fields:
            name_list.append(field.name)
        return name_list

    def get_ip_frac(self):
        ip_parts = str(self.IP).split(".")
        ip_frac = frac((int(ip_parts[0]) * 3) + int(ip_parts[1], 3))
        return ip_frac

    # def save(self, *args, **kwargs):
    #     formatted_avg = round(float(str(self.AVG).lstrip('0')), 3)
    #     self.AVG = float(formatted_avg)
    #     formatted_slg = round(float(str(self.SLG).lstrip('0')), 3)
    #     self.SLG = float(formatted_slg)
    #     formatted_obp = round(float(str(self.OBP).lstrip('0')), 3)
    #     self.OBP = float(formatted_obp)
    #     formatted_ops = round(float(str(self.OPS).lstrip('0')), 3)
    #     self.OPS = float(formatted_ops)
    #     print("Player: " + str(self.player))
    #     print("OPS: " + str(self.OPS))
