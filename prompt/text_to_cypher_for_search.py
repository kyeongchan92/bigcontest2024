NEO4J_SCHEMA = """Node properties:
STORE {
  MCT_NM: STRING. 가맹점명. ex) "토평골식당",
  ADDR: STRING. 가맹점 주소. ex) "제주 서귀포시 토평동 1245-7번지",
  MCT_TYPE: STRING. 요식관련 30개업종. ex) '가정식', '단품요리 전문', '커피', '베이커리', '일식', '치킨', '중식', '분식', '햄버거', '양식', '맥주/요리주점', '아이스크림/빙수', '피자', '샌드위치/토스트', '차', '꼬치구이', '기타세계요리', '구내식당/푸드코트', '떡/한과', '도시락', '도너츠', '주스', '동남아/인도음식', '패밀리 레스토랑', '기사식당', '야식', '스테이크', '포장마차', '부페', '민속주점'
  OP_YMD: STRING. 가맹점개설일자. ex)"20050704"
}
MONTH {
  YM: STRING. 기준연월. ex) "202306",
  month: STRING. 월 이름. ex) "June"
}
Region {
  name: STRING. 지역명. ex) "대포동", "서홍동", "대정읍"
}
City {
  name: STRING. 도시명. ex) "서귀포시", "제주시"
}

Relationship properties:
USE {
  UE_CNT_GRP: 이용건수구간. 월별 이용건수를 6개 구간으로 집계 시, 해당 가맹점의 이용건수가 포함되는 분위수 구간. ex)'상위 10% 이하', '10~25%', '25~50%', '50~75%', '75~90%', '90% 초과(하위 10% 이하)'
  UE_AMT_GRP: 이용금액구간. 월별 이용금액을 6개 구간으로 집계 시, 해당 가맹점의 이용금액이 포함되는 분위수 구간. ex)'상위 10% 이하', '10~25%', '25~50%', '50~75%', '75~90%', '90% 초과(하위 10% 이하)'
  UE_AMT_PER_TRSN_GRP: 건당 평균 이용금액 구간. 월별 건당 평균 이용금액을 6개 구간으로 집계 시, 해당 가맹점의 건당 평균 이용금액이 포함되는 분위수 구간. ex)'상위 10% 이하', '10~25%', '25~50%', '50~75%', '75~90%', '90% 초과(하위 10% 이하)'
  MON_UE_CNT_RAT: 월요일 이용건수 비중. FLOAT. ex) 0.1262
  TUE_UE_CNT_RAT: 화요일 이용건수 비중. FLOAT. ex) 0.1262
  WED_UE_CNT_RAT: 수요일 이용건수 비중. FLOAT. ex) 0.1941
  THU_UE_CNT_RAT: 목요일 이용건수 비중. FLOAT. ex) 0.2233
  FRI_UE_CNT_RAT: 금요일 이용건수 비중. FLOAT. ex) 0.1553
  SAT_UE_CNT_RAT: 토요일 이용건수 비중. FLOAT. ex) 0.1747
  SUN_UE_CNT_RAT: 일요일 이용건수 비중. FLOAT. ex) 0.1818

  # 시간대별
  HR_5_11_UE_CNT_RAT: 5시~11시 이용건수 비중. FLOAT. ex) 0.1650
  HR_12_13_UE_CNT_RAT: 12시~13시 이용건수 비중. FLOAT. ex) 0.5242
  HR_14_17_UE_CNT_RAT: 14시~17시 이용건수 비중. FLOAT. ex) 0.3107
  HR_18_22_UE_CNT_RAT: 18시~22시 이용건수 비중. FLOAT. ex) 0.0511
  HR_23_4_UE_CNT_RAT: 23시~4시 이용건수 비중. FLOAT. ex) 0.07313

  # 현지인
  LOCAL_UE_CNT_RAT: 현지인 이용건수 비중. FLOAT. ex) 0.5843

  # 성별
  RC_M12_MAL_CUS_CNT_RAT: 남성 이용건수 비중. FLOAT. ex) 0.634
  RC_M12_FME_CUS_CNT_RAT: 여성 이용건수 비중. FLOAT. ex) 0.366

  # 연령대별
  RC_M12_AGE_UND_20_CUS_CNT_RAT: 20대 이하 이용건수 비중. FLOAT. ex) 0.066
  RC_M12_AGE_30_CUS_CNT_RAT: 30대 이용건수 비중. FLOAT. ex) 0.252
  RC_M12_AGE_40_CUS_CNT_RAT: 40대 이용건수 비중. FLOAT. ex) 0.398
  RC_M12_AGE_50_CUS_CNT_RAT: 50대 이용건수 비중. FLOAT. ex) 0.201
  RC_M12_AGE_OVR_60_CUS_CNT_RAT: 60대 이상 이용건수 비중. FLOAT. ex) 0.083
}
HAS_STORE {}
HAS_REGION {}

The relationships:
(:City)-[:HAS_REGION]->(:Region)
(:REGION)-[:HAS_STORE]->(:STORE)
(:STORE)-[:USE]->(:MONTH)"""


# 예제 생성 기준 : 연월포함(1), 연월미포함(2) - 수치형[평균], 범주형[최근], 어려운질문(1)
EXAMPLES = [
    """USER INPUT: '23년 10월 기준으로 제주시 한림읍에 있는 카페 중 30대 이용 비중이 가장 높은곳은 ?' QUERY: MATCH (c:City)-[:HAS_REGION]->(r:Region)-[:HAS_STORE]->(s:STORE)-[u:USE]->(m:MONTH)
WHERE c.name = '제주시'
  AND r.name = '한림읍'
  AND s.MCT_TYPE = "커피"
  AND m.YM = 202310
WITH s, u.RC_M12_AGE_30_CUS_CNT_RAT AS age_30_ratio
RETURN s.MCT_NM, age_30_ratio
ORDER BY age_30_ratio DESC
LIMIT 1""",    
    """USER INPUT: '제주시 한림읍에 있는 카페 중 30대 이용 비중이 가장 높은 곳은?' QUERY: MATCH (c:City)-[:HAS_REGION]->(r:Region)-[:HAS_STORE]->(s:STORE)-[u:USE]->(m:MONTH)
WHERE c.name = '제주시'
  AND r.name = '한림읍'
  AND s.MCT_TYPE = "커피"
WITH s, avg(u.RC_M12_AGE_30_CUS_CNT_RAT) AS avg_age_30_ratio
RETURN s.MCT_NM, avg_age_30_ratio
ORDER BY avg_age_30_ratio DESC
LIMIT 1""",
    """USER INPUT: '제주시 노형동에 있는 단품요리 전문점 중 이용건수 구간이 상위 10% 이하에 속하고 현지인 이용 비중이 가장 높은 곳은?' QUERY: MATCH (c:City)-[:HAS_REGION]->(r:Region)-[:HAS_STORE]->(s:STORE)-[u:USE]->(m:MONTH)
WHERE c.name = '제주시'
  AND r.name = '노형동'
  AND s.MCT_TYPE = '단품요리 전문'
  ORDER BY m.YM DESC
WITH s, collect(u.UE_CNT_GRP)[0] AS last_usage_count_group, avg(u.LOCAL_UE_CNT_RAT) AS avg_local_ratio
WHERE last_usage_count_group = '상위 10% 이하'
RETURN s.MCT_NM, avg_local_ratio
ORDER BY avg_local_ratio DESC
LIMIT 1""",
    """USER INPUT: '제주시 카페 중 이용건수 구간이 10~25%, 이용금액 구간은 25~50%에 속하고 오후 2시에서 5시 사이 이용건수 비중이 30% 이상이며 여성이용 비중은 30% 이상인 곳 중에 30대 이용건수 비중이 가장 높은 두 곳은?' MATCH (c:City)-[:HAS_REGION]->(r:Region)-[:HAS_STORE]->(s:STORE)-[u:USE]->(m:MONTH)
WHERE c.name = '제주시'
  AND s.MCT_TYPE = '커피'
  ORDER BY m.YM DESC
WITH s, collect(u.UE_CNT_GRP)[0] AS last_usage_count_group, collect(u.UE_AMT_GRP)[0] AS last_usage_amount_group, avg(u.HR_14_17_UE_CNT_RAT) AS avg_14_17_usage_count_ratio, avg(u.RC_M12_FME_CUS_CNT_RAT) AS avg_female_ratio, avg(u.RC_M12_AGE_30_CUS_CNT_RAT) AS avg_age_30_ratio
WHERE last_usage_count_group = '10~25%' 
  AND last_usage_amount_group = '25~50%'
  AND avg_14_17_usage_count_ratio >= 0.3 
  AND avg_female_ratio >= 0.3
RETURN s.MCT_NM, avg_age_30_ratio
ORDER BY avg_age_30_ratio DESC
LIMIT 2"""
]


# (v2) 예제 생성 기준 : 연월포함(1), 연월미포함(2) - 수치형[평균], 범주형[최근], 어려운질문(1) > 최대한 안겹치게 예제 수정
EXAMPLES_v2 = [
    """USER INPUT: '23년 10월 기준으로 제주시 한림읍에 있는 카페 중 30대 이용 비중이 가장 높은곳은 ?' QUERY: MATCH (c:City)-[:HAS_REGION]->(r:Region)-[:HAS_STORE]->(s:STORE)-[u:USE]->(m:MONTH)
WHERE c.name = '제주시'
  AND r.name = '한림읍'
  AND s.MCT_TYPE = '커피'
  AND m.YM = 202310
WITH s, u.RC_M12_AGE_30_CUS_CNT_RAT AS age_30_ratio
RETURN s.MCT_NM, age_30_ratio
ORDER BY age_30_ratio DESC
LIMIT 1""",    
    """USER INPUT: '서귀포시 안덕면의 중국집에서 가장 높은 화요일 이용 비중인 곳은?' QUERY: MATCH (c:City)-[:HAS_REGION]->(r:Region)-[:HAS_STORE]->(s:STORE)-[u:USE]->(m:MONTH)
WHERE c.name = '서귀포시'
  AND r.name = '안덕면'
  AND s.MCT_TYPE = '중식'
WITH s, avg(u.TUE_UE_CNT_RAT) AS avg_tuesday_ratio
RETURN s.MCT_NM, avg_tuesday_ratio
ORDER BY avg_tuesday_ratio DESC
LIMIT 1""",
    """USER INPUT: '제주시 노형동에 있는 단품요리 전문점 중 이용건수가 상위 10%에 속하고 현지인 이용 비중이 가장 높은 곳은?' QUERY: MATCH (c:City)-[:HAS_REGION]->(r:Region)-[:HAS_STORE]->(s:STORE)-[u:USE]->(m:MONTH)
WHERE c.name = '제주시'
  AND r.name = '노형동'
  AND s.MCT_TYPE = '단품요리 전문'
  ORDER BY m.YM DESC
WITH s, collect(u.UE_CNT_GRP)[0] AS last_usage_count_group, avg(u.LOCAL_UE_CNT_RAT) AS avg_local_ratio
WHERE last_usage_count_group = '상위 10% 이하'
RETURN s.MCT_NM, avg_local_ratio
ORDER BY avg_local_ratio DESC
LIMIT 1""",
    """USER INPUT: '서귀포시 빵집 중에 이용건수 구간이 10~25%, 이용금액 구간은 25~50%에 해당하고 오후 2시에서 5시 사이의 이용 비중이 30% 이상이며 여성이용 비중은 30% 이상인 곳 중에 60대 이상 이용비중이 가장 높은 두 곳은?' QUERY: MATCH (c:City)-[:HAS_REGION]->(r:Region)-[:HAS_STORE]->(s:STORE)-[u:USE]->(m:MONTH)
WHERE c.name = '서귀포시'
  AND s.MCT_TYPE = '베이커리'
  ORDER BY m.YM DESC
WITH s, collect(u.UE_CNT_GRP)[0] AS last_usage_count_group, collect(u.UE_AMT_GRP)[0] AS last_usage_amount_group, avg(u.HR_14_17_UE_CNT_RAT) AS avg_14_17_usage_count_ratio, avg(u.RC_M12_FME_CUS_CNT_RAT) AS avg_female_ratio, avg(u.RC_M12_AGE_OVR_60_CUS_CNT_RAT) AS avg_age_60_ratio
WHERE last_usage_count_group = '10~25%' 
  AND last_usage_amount_group = '25~50%'
  AND avg_14_17_usage_count_ratio >= 0.3 
  AND avg_female_ratio >= 0.3
RETURN s.MCT_NM, avg_age_60_ratio
ORDER BY avg_age_60_ratio DESC
LIMIT 2"""
]


EXAMPLES_COMBINED = '\n'.join(EXAMPLES_v2) if EXAMPLES_v2 else ''

TEXT_TO_CYPHER_FOR_SEARCH_TEMPLATE = """Task: Generate a Cypher statement for querying a Neo4j graph database from a user input.

Schema:
{NEO4J_SCHEMA}

Examples (optional):
{EXAMPLES_COMBINED}

Input:
{query}

Never use any properties or relationships not included in the schema.
Never include triple backticks ```.
Add an appropriate LIMIT clause.

Cypher query:"""