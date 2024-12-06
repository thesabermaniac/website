
        context = super().get_context_data(**kwargs)

        # Fetch data for hitters and pitchers based on the query
        query = Q(year=2025, projection_system='steamer') | Q(year=2026, projection_system='zips')
        hitters = HittingStatistics.objects.filter(query)
        pitchers = PitchingStatistics.objects.filter(query)
        all_stats = list(chain(hitters, pitchers))
        hitting_stats = ['fOPS', 'fAVG', 'fR', 'fRBI', 'fHR', 'fSB']
        pitching_stats = ['fERA', 'fWHIP', 'fW', 'fSO', 'fSVH', 'fK_BB']
        # players = {s.player for s in all_stats}

        player_stats = defaultdict(lambda: defaultdict(list))
        for stat in all_stats:
            player_stats[stat.player][stat.year].append(stat)

        player_id_map = []
        fScores = defaultdict(dict)
        for player, years in player_stats.items():
            player_id_map.append({'name': player.name, 'fangraphs_id': player.fangraphs_id})
            for year, stats in years.items():
                hitting_total = 0
                pitching_total = 0
                for stat in stats:
                    if type(stat) == HittingStatistics:
                        hitting_total = self.calculate_fScores(stat, hitting_stats)
                    elif type(stat) == PitchingStatistics:
                        pitching_total = self.calculate_fScores(stat, pitching_stats)
                fscore = hitting_total + pitching_total
                fScores[player.fangraphs_id][year] = fscore
        context['fScores'] = fScores
        context['players'] = player_id_map

        # # Generate hitting and pitching fScores
        # hitting_fScores = self.calculate_fScores(hitters, [
        #     'fOPS', 'fAVG', 'fR', 'fRBI', 'fHR', 'fSB'
        # ])
        # pitching_fScores = self.calculate_fScores(pitchers, [
        #     'fERA', 'fWHIP', 'fW', 'fSO', 'fSVH', 'fK_BB'
        # ])
        # context['fScores'] = hitting_fScores.update(pitching_fScores)

        # Teams for the template
        context['teams'] = [
            {'name': 'Team A', 'form_id': 'trade_form1'},
            {'name': 'Team B', 'form_id': 'trade_form2'},
        ]

        return context

    def calculate_fScores(self, stat, attributes):
        """
        Calculate fScores for players based on specified attributes.
        """
        # fScores = {}
        # player_id = stat.player.fangraphs_id
        # if player_id not in fScores:
        #     fScores[player_id] = {}
        # fScores[player_id][stat.year] = round(
        #     sum(getattr(stat, attr, 0) for attr in attributes) / len(attributes)
        # )
        # return fScores
        return round(
            sum(getattr(stat, attr, 0) for attr in attributes) / len(attributes)
        )