select 
	tlsp.idPlayer as id_player,
	tp.descCountry as pais_origem_player,
	TIMESTAMPDIFF(YEAR, tp.dtBirth, CURDATE()) as idade_player,
	tlsp.qtKill/tlsp.qtDeath as rating_kd
from
	tb_lobby_stats_player tlsp
left join tb_players tp on tp.idPlayer = tlsp.idPlayer 
group by tlsp.idPlayer;

