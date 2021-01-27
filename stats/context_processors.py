from stats.models import PitchingStatistics, HittingStatistics


def years_processor(request):
    hitting_years = HittingStatistics.objects.filter(is_projection=False).order_by().values_list('year', flat=True).distinct()
    pitching_years = PitchingStatistics.objects.filter(is_projection=False).order_by().values_list('year', flat=True).distinct()
    bigboard_years = list(set(HittingStatistics.objects.filter(is_projection=False).order_by().values_list('year', flat=True).distinct()) & set(PitchingStatistics.objects.filter(is_projection=False).order_by().values_list('year', flat=True).distinct()))
    return {'hitting_years': hitting_years,'pitching_years': pitching_years, 'bigboard_years': bigboard_years}


def years_processor_proj(request):
    hitting_years_proj = HittingStatistics.objects.filter(is_projection=True, projection_system="steamer").order_by().values_list('year', flat=True).distinct()
    pitching_years_proj = PitchingStatistics.objects.filter(is_projection=True, projection_system="steamer").order_by().values_list('year', flat=True).distinct()
    bigboard_years_proj = list(set(HittingStatistics.objects.filter(is_projection=True, projection_system="steamer").order_by().values_list('year', flat=True).distinct()) & set(PitchingStatistics.objects.filter(is_projection=True, projection_system="steamer").order_by().values_list('year', flat=True).distinct()))
    return {'hitting_years_proj': hitting_years_proj,'pitching_years_proj': pitching_years_proj, 'bigboard_years_proj': bigboard_years_proj}
