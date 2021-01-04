import mydao
import collectData
import requests
import time

#데이터베이스 접근 mydao.MyDAO // api키 관리 collectData.CollectData
class MatchDto(mydao.MyDAO,collectData.CollectData) :
    #MatchDto 테이블 생성
    def createTables(self):
        self.connectDB()
        sql =   '''
                CREATE TABLE IF NOT EXISTS `team_easy`.`matchDto` (
                  `gameId` BIGINT NOT NULL,
                  `queueId` INT NULL,
                  `gameType` VARCHAR(20) NULL,
                  `gameDuration` BIGINT NULL,
                  `platformId` VARCHAR(10) NULL,
                  `gameCreation` BIGINT NULL,
                  `seasonId` INT NULL,
                  `gameVersion` VARCHAR(20) NULL,
                  `mapId` INT NULL,
                  `gameMode` VARCHAR(20) NULL,
                  PRIMARY KEY (`gameId`))
                ENGINE = InnoDB
                '''
        self.cur.execute(sql)
        self.conn.commit()
        print('create matchDto table.')
        sql = '''
                CREATE TABLE IF NOT EXISTS `team_easy`.`playerDto` (
                  `gameId` BIGINT NOT NULL,
                  `participantId` INT NOT NULL,
                  `profileIcon` INT NULL,
                  `accountId` VARCHAR(100) NULL,
                  `matchHistoryUri` VARCHAR(100) NULL,
                  `currentAccountId` VARCHAR(100) NULL,
                  `currentPlatformId` VARCHAR(10) NULL,
                  `summonerName` VARCHAR(50) NULL,
                  `summonerId` VARCHAR(100) NULL,
                  `platformId` VARCHAR(10) NULL,
                  PRIMARY KEY (`gameId`, `participantId`),
                  CONSTRAINT `fk_playerDto_matchDto`
                    FOREIGN KEY (`gameId`)
                    REFERENCES `team_easy`.`matchDto` (`gameId`)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE)
                ENGINE = InnoDB
        '''
        self.cur.execute(sql)
        self.conn.commit()
        print('create playerDto table.')
        sql = '''
                CREATE TABLE IF NOT EXISTS `team_easy`.`teamStatsDto` (
                  `gameId` BIGINT NOT NULL,
                  `teamId` INT NOT NULL,
                  `towerKills` INT NULL,
                  `riftHeraldKills` INT NULL,
                  `firstBlood` TINYINT NULL,
                  `inhibitorKills` INT NULL,
                  `bans` VARCHAR(200) NULL,
                  `firstBaron` TINYINT NULL,
                  `firstDragon` TINYINT NULL,
                  `dominionVictoryScore` INT NULL,
                  `dragonKills` INT NULL,
                  `baronKills` INT NULL,
                  `firstInhibitor` TINYINT NULL,
                  `firstTower` TINYINT NULL,
                  `vilemawKills` INT NULL,
                  `firstRiftHerald` TINYINT NULL,
                  `win` VARCHAR(10) NULL,
                  PRIMARY KEY (`gameId`, `teamId`),
                  CONSTRAINT `fk_teamStatsDto_matchDto1`
                    FOREIGN KEY (`gameId`)
                    REFERENCES `team_easy`.`matchDto` (`gameId`)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE)
                ENGINE = InnoDB
        '''
        self.cur.execute(sql)
        self.conn.commit()
        print('create teamStatsDto table.')
        sql = '''
                CREATE TABLE IF NOT EXISTS `team_easy`.`participantDto` (
                  `gameId` BIGINT NOT NULL,
                  `participantId` INT NOT NULL,
                  `championId` INT NULL,
                  `runes` MEDIUMTEXT NULL,
                  `teamId` INT NULL,
                  `spell1Id` INT NULL,
                  `spell2Id` INT NULL,
                  `highestAchievedSeasonTier` VARCHAR(20) NULL,
                  `masteries` MEDIUMTEXT NULL,
                  PRIMARY KEY (`gameId`, `participantId`),
                  CONSTRAINT `fk_participantDto_matchDto1`
                    FOREIGN KEY (`gameId`)
                    REFERENCES `team_easy`.`matchDto` (`gameId`)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE)
                ENGINE = InnoDB
        '''
        self.cur.execute(sql)
        self.conn.commit()
        print('create participantDto table.')
        sql = '''
                CREATE TABLE IF NOT EXISTS `team_easy`.`participantStatsDto` (
                  `gameId` BIGINT NOT NULL,
                  `participantId` INT NOT NULL,
                  `item0` INT NULL,
                  `item2` INT NULL,
                  `totalUnitsHealed` INT NULL,
                  `item1` INT NULL,
                  `largestMultiKill` INT NULL,
                  `goldEarned` INT NULL,
                  `firstInhibitorKill` TINYINT NULL,
                  `physicalDamageTaken` BIGINT NULL,
                  `nodeNeutralizeAssist` INT NULL,
                  `totalPlayerScore` INT NULL,
                  `champLevel` INT NULL,
                  `damageDealtToObjectives` BIGINT NULL,
                  `totalDamageTaken` BIGINT NULL,
                  `neutralMinionsKilled` INT NULL,
                  `deaths` INT NULL,
                  `tripleKills` INT NULL,
                  `magicDamageDealtToChampions` BIGINT NULL,
                  `wardsKilled` INT NULL,
                  `pentaKills` INT NULL,
                  `damageSelfMitigated` BIGINT NULL,
                  `largestCriticalStrike` INT NULL,
                  `nodeNeutralize` INT NULL,
                  `totalTimeCrowdControlDealt` INT NULL,
                  `firstTowerKill` TINYINT NULL,
                  `magicDamageDealt` BIGINT NULL,
                  `totalScoreRank` INT NULL,
                  `nodeCapture` INT NULL,
                  `wardsPlaced` INT NULL,
                  `totalDamageDealt` BIGINT NULL,
                  `timeCCingOthers` BIGINT NULL,
                  `magicalDamageTaken` BIGINT NULL,
                  `largestKillingSpree` INT NULL,
                  `totalDamageDealtToChampions` BIGINT NULL,
                  `physicalDamageDealtToChampions` BIGINT NULL,
                  `neutralMinionsKilledTeamJungle` INT NULL,
                  `totalMinionsKilled` INT NULL,
                  `firstInhibitorAssist` TINYINT NULL,
                  `visionWardsBoughtInGame` INT NULL,
                  `objectivePlayerScore` INT NULL,
                  `kills` INT NULL,
                  `firstTowerAssist` TINYINT NULL,
                  `combatPlayerScore` INT NULL,
                  `inhibitorKills` INT NULL,
                  `turretKills` INT NULL,
                  `trueDamageTaken` BIGINT NULL,
                  `firstBloodAssist` TINYINT NULL,
                  `nodeCaptureAssist` INT NULL,
                  `assists` INT NULL,
                  `teamObjective` INT NULL,
                  `altarsNeutralized` INT NULL,
                  `goldSpent` INT NULL,
                  `damageDealtToTurrets` BIGINT NULL,
                  `altarsCaptured` INT NULL,
                  `win` TINYINT NULL,
                  `totalHeal` BIGINT NULL,
                  `unrealKills` INT NULL,
                  `visionScore` BIGINT NULL,
                  `physicalDamageDealt` BIGINT NULL,
                  `firstBloodKill` TINYINT NULL,
                  `longestTimeSpentLiving` INT NULL,
                  `killingSprees` INT NULL,
                  `sightWardsBoughtInGame` INT NULL,
                  `trueDamageDealtToChampions` BIGINT NULL,
                  `neutralMinionsKilledEnemyJungle` INT NULL,
                  `doubleKills` INT NULL,
                  `trueDamageDealt` BIGINT NULL,
                  `quadraKills` INT NULL,
                  `item4` INT NULL,
                  `item3` INT NULL,
                  `item6` INT NULL,
                  `item5` INT NULL,
                  `playerScore0` INT NULL,
                  `playerScore1` INT NULL,
                  `playerScore2` INT NULL,
                  `playerScore3` INT NULL,
                  `playerScore4` INT NULL,
                  `playerScore5` INT NULL,
                  `playerScore6` INT NULL,
                  `playerScore7` INT NULL,
                  `playerScore8` INT NULL,
                  `playerScore9` INT NULL,
                  `perk0` INT NULL,
                  `perk0Var1` INT NULL,
                  `perk0Var2` INT NULL,
                  `perk0Var3` INT NULL,
                  `perk1` INT NULL,
                  `perk1Var1` INT NULL,
                  `perk1Var2` INT NULL,
                  `perk1Var3` INT NULL,
                  `perk2` INT NULL,
                  `perk2Var1` INT NULL,
                  `perk2Var2` INT NULL,
                  `perk2Var3` INT NULL,
                  `perk3` INT NULL,
                  `perk3Var1` INT NULL,
                  `perk3Var2` INT NULL,
                  `perk3Var3` INT NULL,
                  `perk4` INT NULL,
                  `perk4Var1` INT NULL,
                  `perk4Var2` INT NULL,
                  `perk4Var3` INT NULL,
                  `perk5` INT NULL,
                  `perk5Var1` INT NULL,
                  `perk5Var2` INT NULL,
                  `perk5Var3` INT NULL,
                  `perkPrimaryStyle` INT NULL,
                  `perkSubStyle` INT NULL,
                  `statPerk0` INT NULL,
                  `statPerk1` INT NULL,
                  `statPerk2` INT NULL,
                  PRIMARY KEY (`gameId`, `participantId`),
                  CONSTRAINT `fk_participantStatsDto_participantDto1`
                    FOREIGN KEY (`gameId` , `participantId`)
                    REFERENCES `team_easy`.`participantDto` (`gameId` , `participantId`)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE)
                ENGINE = InnoDB
        '''
        self.cur.execute(sql)
        self.conn.commit()
        print('create participantStatsDto table.')
        sql = '''
                CREATE TABLE IF NOT EXISTS `team_easy`.`participantTimelineDto` (
                  `gameId` BIGINT NOT NULL,
                  `participantId` INT NOT NULL,
                  `csDiffPerMinDeltas` JSON NULL,
                  `damageTakenPerMinDeltas` JSON NULL,
                  `role` VARCHAR(20) NULL,
                  `damageTakenDiffPerMinDeltas` JSON NULL,
                  `xpPerMinDeltas` JSON NULL,
                  `xpDiffPerMinDeltas` JSON NULL,
                  `lane` VARCHAR(10) NULL,
                  `creepsPerMinDeltas` JSON NULL,
                  `goldPerMinDeltas` JSON NULL,
                  PRIMARY KEY (`gameId`, `participantId`),
                  CONSTRAINT `fk_participantTimelineDto_participantDto1`
                    FOREIGN KEY (`gameId` , `participantId`)
                    REFERENCES `team_easy`.`participantDto` (`gameId` , `participantId`)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE)
                ENGINE = InnoDB
        '''
        self.cur.execute(sql)
        self.conn.commit()
        print('create participantTimelineDto table.')
        self.closeDB()

    #데이터베이스에서 matchReferenceDto들을 얻어온다 start_num은 시작할 인덱스, amount는 몇개 출력
    def getMatchReferenceDtos(self,start_num,amount):
        self.connectDB()
        sql = f'SELECT * FROM matchReferenceDto LIMIT {start_num}, {amount}'
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        self.closeDB()
        return rows

    #gameId로 MatchDto를 받아온다
    def getMatchDtoFromApi(self,gameId):
        # path = 'apikey.txt'
        # self.setApikeyFromFile(path)
        uri = f'https://kr.api.riotgames.com/lol/match/v4/matches/{gameId}?api_key={self.api_key}'
        print(uri)
        response = requests.get(uri)
        status_code = response.status_code
        data = response.json()
        return status_code, data

    #matchReferenceDto 테이블을 채운다. api에서 받은 데이터를 insert를 반복하여 채움
    def insertMatchDtos(self):
        self.setApikeyFromFile()
        start_num =0
        amount=1000
        while True :
            rows=self.getMatchReferenceDtos(start_num,amount)
            if len(rows) == 0 :
                break
            max_row = len(rows)
            row_index =0
            while row_index < max_row :
                row =rows[row_index]
                gameId =row[0]
                status_code, data = self.getMatchDtoFromApi(gameId)
                if status_code == 200 : #데이터 받는데 성공
                    self.insertMatchDto(data)
                elif status_code == 429 : #사용량 제한 걸림
                    self.changeApikey()
                    continue
                row_index+=1
            start_num += amount

    #하나의 matchReferenceDto를 insert한다
    def insertMatchDto(self,dto):
        self.connectDB()
        print('type : ', type(dto), ' data : ', dto)
        gameId = dto['gameId']
        teams = dto.pop('teams')
        participants = dto.pop('participants')
        participantIdentities = dto.pop('participantIdentities')
        keys = list(dto.keys())
        values = list(dto.values())
        print('teams :', teams)
        print('participants :', participants)
        print('participantIdentities : ',participantIdentities)

        #matchDto 테이블에 데이터 넣기
        gameVersion =dto['gameVersion']
        print(gameVersion)
        if gameVersion.startswith('10.') :
            p_list = ['%s' for _ in range(len(values))]
            sql = 'REPLACE INTO matchDto('
            sql += ','.join(keys)
            sql += ') VALUES('
            sql += ','.join(p_list)
            sql += ')'
            print(sql)
            print(values)
            self.cur.execute(sql,values)

            #teamstatsDto에 데이터 넣기
            for team in teams :
                team_keys = ['gameId']
                team_keys.extend(team.keys())
                team_values = [gameId]
                team_values.extend(list(team.values()))
                for i,v in enumerate(team_values) :
                    team_values[i] = self.transformForDB(v)
                p_list = ['%s' for _ in range(len(team_values))]
                sql = 'REPLACE INTO teamStatsDto('
                sql += ','.join(team_keys)
                sql += ') VALUES('
                sql += ','.join(p_list)
                sql += ')'
                self.cur.execute(sql, team_values)

            #participantIdentities (playerDto)에 데이터 넣기
            for participantIdentity in participantIdentities :
                participantId = participantIdentity['participantId']
                player = participantIdentity['player']
                player_keys = player.keys()
                player_values = list(player.values())
                participantIdentity_keys = ['gameId','participantId']
                participantIdentity_keys.extend(player_keys)
                participantIdentity_values = [gameId,participantId]
                participantIdentity_values.extend(player_values)
                p_list = ['%s' for _ in range(len(participantIdentity_values))]
                sql = 'REPLACE INTO playerDto('
                sql += ','.join(participantIdentity_keys)
                sql += ') VALUES('
                sql += ','.join(p_list)
                sql += ')'
                self.cur.execute(sql, participantIdentity_values)

            #participants (participantDto)에 데이터 넣기
            for participant in participants :
                stats = participant.pop('stats')
                timeline = participant.pop('timeline')
                participant_keys = ['gameId']
                participant_keys.extend(participant.keys())
                participant_values = [gameId]
                participant_values.extend(list(participant.values()))
                p_list = ['%s' for _ in range(len(participant_values))]
                sql = 'REPLACE INTO participantDto('
                sql += ','.join(participant_keys)
                sql += ') VALUES('
                sql += ','.join(p_list)
                sql += ')'
                self.cur.execute(sql, participant_values)

                #participantStatsDto에 값 넣기
                stats_keys= ['gameId']
                stats_keys.extend(stats.keys())
                stats_values = [gameId]
                stats_values.extend(list(stats.values()))
                p_list = ['%s' for _ in range(len(stats_values))]
                sql = 'REPLACE INTO participantStatsDto('
                sql += ','.join(stats_keys)
                sql += ') VALUES('
                sql += ','.join(p_list)
                sql += ')'
                self.cur.execute(sql, stats_values)

                #participantTimelineDto에 값 넣기
                timeline_keys = ['gameId']
                timeline_keys.extend(timeline.keys())
                timeline_values = [gameId]
                timeline_values.extend(list(timeline.values()))
                for i,v in enumerate(timeline_values) :
                    timeline_values[i] = self.transformForDB(v)
                p_list = ['%s' for _ in range(len(timeline_values))]
                sql = 'REPLACE INTO participantTimelineDto('
                sql += ','.join(timeline_keys)
                sql += ') VALUES('
                sql += ','.join(p_list)
                sql += ')'
                self.cur.execute(sql, timeline_values)

            #변경된 내용 저장하기
            self.conn.commit()
        else :
            print('구버전 ',gameVersion)
        self.closeDB()


#메인함수
if __name__ == '__main__':
    matchDto = MatchDto()
    matchDto.createTables()
    # start_time = time.time()
    matchDto.insertMatchDtos()
    # end_time = time.time()
    # print('총 수행 시간 : %.2f초'%(end_time-start_time))


#match 기본 테이블, gameId를 얻는다
'''
CREATE TABLE IF NOT EXISTS `team_easy`.`matchDto` (
  `gameId` BIGINT NOT NULL,
  `queueId` INT NULL,
  `gameType` VARCHAR(20) NULL,
  `gameDuration` BIGINT NULL,
  `platformId` VARCHAR(10) NULL,
  `gameCreation` BIGINT NULL,
  `seasonId` INT NULL,
  `gameVersion` VARCHAR(20) NULL,
  `mapId` INT NULL,
  `gameMode` VARCHAR(20) NULL,
  PRIMARY KEY (`gameId`))
ENGINE = InnoDB
'''
#match의 participant정보 , 소환사 이름을 포함한다
'''
CREATE TABLE IF NOT EXISTS `team_easy`.`playerDto` (
  `gameId` BIGINT NOT NULL,
  `participantId` INT NOT NULL,
  `profileIcon` INT NULL,
  `accountId` VARCHAR(100) NULL,
  `matchHistoryUri` VARCHAR(100) NULL,
  `currentAccountId` VARCHAR(100) NULL,
  `currentPlatformId` VARCHAR(10) NULL,
  `summonerName` VARCHAR(50) NULL,
  `summonerId` VARCHAR(100) NULL,
  `platformId` VARCHAR(10) NULL,
  PRIMARY KEY (`gameId`, `participantId`),
  CONSTRAINT `fk_playerDto_matchDto`
    FOREIGN KEY (`gameId`)
    REFERENCES `team_easy`.`matchDto` (`gameId`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
'''
#match의 teamstat , team 승패 정보
'''
CREATE TABLE IF NOT EXISTS `team_easy`.`teamStatsDto` (
  `gameId` BIGINT NOT NULL,
  `teamId` INT NOT NULL,
  `towerKills` INT NULL,
  `riftHeraldKills` INT NULL,
  `firstBlood` TINYINT NULL,
  `inhibitorKills` INT NULL,
  `bans` VARCHAR(200) NULL,
  `firstBaron` TINYINT NULL,
  `firstDragon` TINYINT NULL,
  `dominionVictoryScore` INT NULL,
  `dragonKills` INT NULL,
  `baronKills` INT NULL,
  `firstInhibitor` TINYINT NULL,
  `firstTower` TINYINT NULL,
  `vilemawKills` INT NULL,
  `firstRiftHerald` TINYINT NULL,
  `win` VARCHAR(10) NULL,
  PRIMARY KEY (`gameId`, `teamId`),
  CONSTRAINT `fk_teamStatsDto_matchDto1`
    FOREIGN KEY (`gameId`)
    REFERENCES `team_easy`.`matchDto` (`gameId`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
'''
#match의 participant의 기본정보, champion을 얻는다
'''
CREATE TABLE IF NOT EXISTS `team_easy`.`participantDto` (
  `gameId` BIGINT NOT NULL,
  `participantId` INT NOT NULL,
  `championId` INT NULL,
  `runes` MEDIUMTEXT NULL,
  `teamId` INT NULL,
  `spell1Id` INT NULL,
  `spell2Id` INT NULL,
  `highestAchievedSeasonTier` VARCHAR(20) NULL,
  `masteries` MEDIUMTEXT NULL,
  PRIMARY KEY (`gameId`, `participantId`),
  CONSTRAINT `fk_participantDto_matchDto1`
    FOREIGN KEY (`gameId`)
    REFERENCES `team_easy`.`matchDto` (`gameId`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
'''
#participant의 stats
'''
CREATE TABLE IF NOT EXISTS `team_easy`.`participantStatsDto` (
  `gameId` BIGINT NOT NULL,
  `participantId` INT NOT NULL,
  `item0` INT NULL,
  `item2` INT NULL,
  `totalUnitsHealed` INT NULL,
  `item1` INT NULL,
  `largestMultiKill` INT NULL,
  `goldEarned` INT NULL,
  `firstInhibitorKill` TINYINT NULL,
  `physicalDamageTaken` BIGINT NULL,
  `nodeNeutralizeAssist` INT NULL,
  `totalPlayerScore` INT NULL,
  `champLevel` INT NULL,
  `damageDealtToObjectives` BIGINT NULL,
  `totalDamageTaken` BIGINT NULL,
  `neutralMinionsKilled` INT NULL,
  `deaths` INT NULL,
  `tripleKills` INT NULL,
  `magicDamageDealtToChampions` BIGINT NULL,
  `wardsKilled` INT NULL,
  `pentaKills` INT NULL,
  `damageSelfMitigated` BIGINT NULL,
  `largestCriticalStrike` INT NULL,
  `nodeNeutralize` INT NULL,
  `totalTimeCrowdControlDealt` INT NULL,
  `firstTowerKill` TINYINT NULL,
  `magicDamageDealt` BIGINT NULL,
  `totalScoreRank` INT NULL,
  `nodeCapture` INT NULL,
  `wardsPlaced` INT NULL,
  `totalDamageDealt` BIGINT NULL,
  `timeCCingOthers` BIGINT NULL,
  `magicalDamageTaken` BIGINT NULL,
  `largestKillingSpree` INT NULL,
  `totalDamageDealtToChampions` BIGINT NULL,
  `physicalDamageDealtToChampions` BIGINT NULL,
  `neutralMinionsKilledTeamJungle` INT NULL,
  `totalMinionsKilled` INT NULL,
  `firstInhibitorAssist` TINYINT NULL,
  `visionWardsBoughtInGame` INT NULL,
  `objectivePlayerScore` INT NULL,
  `kills` INT NULL,
  `firstTowerAssist` TINYINT NULL,
  `combatPlayerScore` INT NULL,
  `inhibitorKills` INT NULL,
  `turretKills` INT NULL,
  `trueDamageTaken` BIGINT NULL,
  `firstBloodAssist` TINYINT NULL,
  `nodeCaptureAssist` INT NULL,
  `assists` INT NULL,
  `teamObjective` INT NULL,
  `altarsNeutralized` INT NULL,
  `goldSpent` INT NULL,
  `damageDealtToTurrets` BIGINT NULL,
  `altarsCaptured` INT NULL,
  `win` TINYINT NULL,
  `totalHeal` BIGINT NULL,
  `unrealKills` INT NULL,
  `visionScore` BIGINT NULL,
  `physicalDamageDealt` BIGINT NULL,
  `firstBloodKill` TINYINT NULL,
  `longestTimeSpentLiving` INT NULL,
  `killingSprees` INT NULL,
  `sightWardsBoughtInGame` INT NULL,
  `trueDamageDealtToChampions` BIGINT NULL,
  `neutralMinionsKilledEnemyJungle` INT NULL,
  `doubleKills` INT NULL,
  `trueDamageDealt` BIGINT NULL,
  `quadraKills` INT NULL,
  `item4` INT NULL,
  `item3` INT NULL,
  `item6` INT NULL,
  `item5` INT NULL,
  `playerScore0` INT NULL,
  `playerScore1` INT NULL,
  `playerScore2` INT NULL,
  `playerScore3` INT NULL,
  `playerScore4` INT NULL,
  `playerScore5` INT NULL,
  `playerScore6` INT NULL,
  `playerScore7` INT NULL,
  `playerScore8` INT NULL,
  `playerScore9` INT NULL,
  `perk0` INT NULL,
  `perk0Var1` INT NULL,
  `perk0Var2` INT NULL,
  `perk0Var3` INT NULL,
  `perk1` INT NULL,
  `perk1Var1` INT NULL,
  `perk1Var2` INT NULL,
  `perk1Var3` INT NULL,
  `perk2` INT NULL,
  `perk2Var1` INT NULL,
  `perk2Var2` INT NULL,
  `perk2Var3` INT NULL,
  `perk3` INT NULL,
  `perk3Var1` INT NULL,
  `perk3Var2` INT NULL,
  `perk3Var3` INT NULL,
  `perk4` INT NULL,
  `perk4Var1` INT NULL,
  `perk4Var2` INT NULL,
  `perk4Var3` INT NULL,
  `perk5` INT NULL,
  `perk5Var1` INT NULL,
  `perk5Var2` INT NULL,
  `perk5Var3` INT NULL,
  `perkPrimaryStyle` INT NULL,
  `perkSubStyle` INT NULL,
  `statPerk0` INT NULL,
  `statPerk1` INT NULL,
  `statPerk2` INT NULL,
  PRIMARY KEY (`gameId`, `participantId`),
  CONSTRAINT `fk_participantStatsDto_participantDto1`
    FOREIGN KEY (`gameId` , `participantId`)
    REFERENCES `team_easy`.`participantDto` (`gameId` , `participantId`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
'''
#participant의 타임라인 정보
'''
CREATE TABLE IF NOT EXISTS `team_easy`.`participantTimelineDto` (
  `gameId` BIGINT NOT NULL,
  `participantId` INT NOT NULL,
  `csDiffPerMinDeltas` JSON NULL,
  `damageTakenPerMinDeltas` JSON NULL,
  `role` VARCHAR(20) NULL,
  `damageTakenDiffPerMinDeltas` JSON NULL,
  `xpPerMinDeltas` JSON NULL,
  `xpDiffPerMinDeltas` JSON NULL,
  `lane` VARCHAR(10) NULL,
  `creepsPerMinDeltas` JSON NULL,
  `goldPerMinDeltas` JSON NULL,
  PRIMARY KEY (`gameId`, `participantId`),
  CONSTRAINT `fk_participantTimelineDto_participantDto1`
    FOREIGN KEY (`gameId` , `participantId`)
    REFERENCES `team_easy`.`participantDto` (`gameId` , `participantId`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
'''