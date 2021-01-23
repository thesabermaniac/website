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

    def get_operable_string(self):
        return self.fName + "_" + self.lName


class HittingStatistics(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField(verbose_name="Year")
    is_projection = models.BooleanField(default=False)
    G = models.PositiveSmallIntegerField(verbose_name="Games Played",
                                         default=0)
    PA = models.PositiveSmallIntegerField(verbose_name="Plate Appearances",
                                          default=0)
    HR = models.PositiveSmallIntegerField(verbose_name="Home Runs",
                                          default=0)
    R = models.PositiveSmallIntegerField(verbose_name="Runs Scored",
                                         default=0)
    RBI = models.PositiveSmallIntegerField(verbose_name="Runs Batted In",
                                           default=0)
    BB = models.PositiveSmallIntegerField(verbose_name="Walks",
                                          default=0)
    IBB = models.PositiveSmallIntegerField(verbose_name="Intentional Walks",
                                           default=0)
    SO = models.PositiveSmallIntegerField(verbose_name="Strike Outs",
                                          default=0)
    HBP = models.PositiveSmallIntegerField(verbose_name="Hits By Pitch",
                                           default=0)
    SF = models.PositiveSmallIntegerField(verbose_name="Sacrifice Flies",
                                          default=0)
    SH = models.PositiveSmallIntegerField(verbose_name="Sacrifice Hits",
                                          default=0)
    GDP = models.PositiveSmallIntegerField(verbose_name="Grounded into Double Plays",
                                           default=0)
    SB = models.PositiveSmallIntegerField(verbose_name="Stolen Bases",
                                          default=0)
    CS = models.PositiveSmallIntegerField(verbose_name="Caught Stealing",
                                          default=0)
    AVG = models.FloatField(verbose_name="Batting Average",
                            default=0.0)
    OBP = models.FloatField(verbose_name="On-Base Percentage",
                            default=0.0)
    SLG = models.FloatField(verbose_name="Slugging Percentage",
                            default=0.0)
    OPS = models.FloatField(verbose_name="On-Base Plus Slugging",
                            default=0.0)
    fG = models.SmallIntegerField(verbose_name="Fantasy Games Played",
                                  default=0)
    fPA = models.SmallIntegerField(verbose_name="Fantasy Plate Appearances",
                                   default=0)
    fHR = models.SmallIntegerField(verbose_name="Fantasy Home Runs",
                                   default=0)
    fR = models.SmallIntegerField(verbose_name="Fantasy Runs Scored",
                                  default=0)
    fRBI = models.SmallIntegerField(verbose_name="Fantasy Runs Batted In",
                                    default=0)
    fBB = models.SmallIntegerField(verbose_name="Fantasy Walks",
                                   default=0)
    fIBB = models.SmallIntegerField(verbose_name="Fantasy Intentional Walks",
                                    default=0)
    fSO = models.SmallIntegerField(verbose_name="Fantasy Strikeouts",
                                   default=0)
    fHBP = models.SmallIntegerField(verbose_name="Fantasy Hit By Pitch",
                                    default=0)
    fSF = models.SmallIntegerField(verbose_name="Fantasy Sacrifice Flies",
                                   default=0)
    fSH = models.SmallIntegerField(verbose_name="Fantasy Sacrifice Hits",
                                   default=0)
    fGDP = models.SmallIntegerField(verbose_name="Fantasy Grounded into Double Plays",
                                    default=0)
    fSB = models.SmallIntegerField(verbose_name="Fantasy Stolen Bases",
                                   default=0)
    fCS = models.SmallIntegerField(verbose_name="Fantasy Caught Stealing",
                                   default=0)
    fAVG = models.SmallIntegerField(verbose_name="Fantasy Batting Average",
                                    default=0)
    fOBP = models.SmallIntegerField(verbose_name="Fantasy On Base Percentage",
                                    default=0)
    fSLG = models.SmallIntegerField(verbose_name="Fantasy Slugging Percentage",
                                    default=0)
    fOPS = models.SmallIntegerField(verbose_name="Fantasy On-Base Plus Slugging",
                                    default=0)
    fTotal = models.SmallIntegerField(verbose_name="Fantasy Total",
                                      default=0)

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

    def __str__(self):
        return self.player.get_operable_string() + "_" + str(self.year)


class PitchingStatistics(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField(verbose_name="Year")
    is_projection = models.BooleanField(default=False)
    W = models.SmallIntegerField(verbose_name="Wins",
                                 default=0)
    L = models.SmallIntegerField(verbose_name="Losses",
                                 default=0)
    ERA = models.FloatField(verbose_name="Earned Run Average",
                            default=0.0)
    WHIP = models.FloatField(verbose_name="Walks + Hits/IP",
                             default=0.0)
    G = models.SmallIntegerField(verbose_name="Games Played",
                                 default=0)
    GS = models.SmallIntegerField(verbose_name="Games Started",
                                  default=0)
    CG = models.SmallIntegerField(verbose_name="Complete Games",
                                  default=0)
    ShO = models.SmallIntegerField(verbose_name="Shutouts",
                                   default=0)
    SV = models.SmallIntegerField(verbose_name="Saves",
                                  default=0)
    HLD = models.SmallIntegerField(verbose_name="Holds",
                                   default=0)
    BS = models.SmallIntegerField(verbose_name="Blown Saves",
                                  default=0)
    IP = models.DecimalField(verbose_name="Innings Pitched",
                             decimal_places=1,
                             max_digits=5,
                             default=0.0)
    TBF = models.SmallIntegerField(verbose_name="Total Batters Faced",
                                   default=0)
    H = models.SmallIntegerField(verbose_name="Hits Allowed",
                                 default=0)
    R = models.SmallIntegerField(verbose_name="Runs Allowed",
                                 default=0)
    ER = models.SmallIntegerField(verbose_name="Earned Runs Allowed",
                                  default=0)
    HR = models.SmallIntegerField(verbose_name="Home Runs Allowed",
                                  default=0)
    BB = models.SmallIntegerField(verbose_name="Walks Allowed",
                                  default=0)
    IBB = models.SmallIntegerField(verbose_name="Intentional Walks Allowed",
                                   default=0)
    HBP = models.SmallIntegerField(verbose_name="Hits By Pitch",
                                   default=0)
    WP = models.SmallIntegerField(verbose_name="Wild Pitches",
                                  default=0)
    SO = models.SmallIntegerField(verbose_name="Strikeouts",
                                  default=0)

    fW = models.SmallIntegerField(verbose_name="Fantasy Wins",
                                  default=0)
    fL = models.SmallIntegerField(verbose_name="Fantasy Losses",
                                  default=0)
    fERA = models.FloatField(verbose_name="Fantasy Earned Run Average",
                             default=0.0)
    fWHIP = models.FloatField(verbose_name="Fantasy Walks + Hits/IP",
                              default=0.0)
    fG = models.SmallIntegerField(verbose_name="Fantasy Games Played",
                                  default=0)
    fGS = models.SmallIntegerField(verbose_name="Fantasy Games Started",
                                   default=0)
    fCG = models.SmallIntegerField(verbose_name="Fantasy Complete Games",
                                   default=0)
    fShO = models.SmallIntegerField(verbose_name="Fantasy Shutouts",
                                    default=0)
    fSV = models.SmallIntegerField(verbose_name="Fantasy Saves",
                                   default=0)
    fHLD = models.SmallIntegerField(verbose_name="Fantasy Holds",
                                    default=0)
    fBS = models.SmallIntegerField(verbose_name="Fantasy Blown Saves",
                                   default=0)
    fIP = models.FloatField(verbose_name="Fantasy Innings Pitched",
                            default=0.0)
    fTBF = models.SmallIntegerField(verbose_name="Fantasy Total Batters Faced",
                                    default=0)
    fH = models.SmallIntegerField(verbose_name="Fantasy Hits Allowed",
                                  default=0)
    fR = models.SmallIntegerField(verbose_name="Fantasy Runs Allowed",
                                  default=0)
    fER = models.SmallIntegerField(verbose_name="Fantasy Earned Runs Allowed",
                                   default=0)
    fHR = models.SmallIntegerField(verbose_name="Fantasy Home Runs Allowed",
                                   default=0)
    fBB = models.SmallIntegerField(verbose_name="Fantasy Walks Allowed",
                                   default=0)
    fIBB = models.SmallIntegerField(verbose_name="Fantasy Intentional Walks Allowed",
                                    default=0)
    fHBP = models.SmallIntegerField(verbose_name="Fantasy Hits By Pitch",
                                    default=0)
    fWP = models.SmallIntegerField(verbose_name="Fantasy Wild Pitches",
                                   default=0)
    fSO = models.SmallIntegerField(verbose_name="Fantasy Strikeouts",
                                   default=0)
    fTotal = models.SmallIntegerField(verbose_name="Fantasy Total",
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
