select 
	tlsp.idPlayer as id_player,
	sum(tlsp.flWinner)/count(tlsp.idPlayer) as taxa_vitoria,
	count(tlsp.idPlayer) as qtd_partidas
from
	tb_lobby_stats_player tlsp
group by tlsp.idPlayer
HAVING count(idPlayer) > 10
order by taxa_vitoria DESC
limit 50;
