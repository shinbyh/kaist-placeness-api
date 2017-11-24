var getUrlParameter = function getUrlParameter(sParam) {
	var sPageURL = decodeURIComponent(window.location.search.substring(1)),
		sURLVariables = sPageURL.split('&'),
		sParameterName,
		i;

	for (i = 0; i < sURLVariables.length; i++) {
		sParameterName = sURLVariables[i].split('=');

		if (sParameterName[0] === sParam) {
			return sParameterName[1] === undefined ? true : sParameterName[1];
		}
	}
};
var getParselParameters = function(args){
	var params = {};
	var args = args;
	for (var d in args){
		var val = getUrlParameter(args[d]);
		if (val != undefined) {
			params[args[d]] = val;
		}
	}
	return params;
}
var maptParamsWords = function (param) {
	var words = {
		'time_kwd' : '시간 키워드',
		'with_kwd' : '동행인 키워드',
		'occasion_kwd' : '상황 키워드',
		'weather_kwd' : '날씨 키워드',
		'mood_kwd' : '분위기 키워드',
		'weight_date' : '시간 가중치',
		'weight_occasion' : '상황 가중치',
		'weight_with' : '동행인 가중치',
		'weight_weather' :'날씨 가중치',
		'weight_mood' : '분위기 가중치',
		'topk' : '가져오는 개수',
		"rain_normal" :"비 평균",
		"rain_no" :"비 없음",
		"rain_low" :"비 조금",
		"rain_high" :"비 많이",

		"temp_normal":"온도 평균",
		"temp_low" :"온도 낮음",
		"temp_high" :"온도 높음",

		"wind_normal" :"바람 평균",
		"wind_high" :"바람 심함",

		"snow_normal" :"눈 평균",
		"snow_no" :"눈 없음",
		"snow_low" :"눈 조금",
		"snow_high" :"눈 많이",

		"Mood_전통적" :"전통적",
		"Mood_세련된" :"세련된",
		"Mood_답답한" :"답답한",
		"Mood_친절한" :"친절한",
		"Mood_편안한" :"편안한",
		"Mood_로맨틱한" :"로멘틱한",
		"Mood_북적이는" :"북적이는",

		"Occasion_카페" :"카페",
		"Occasion_운동" :"운동",
		"Occasion_회식" :"회식",
		"Occasion_의료" :"의료",
		"Occasion_집안일" :"집안일",
		"Occasion_휴식" :"휴식",
		"Occasion_문화생활" :"문화생활",
		"Occasion_나들이" :"나들이",
		"Occasion_맛집탐방" :"맛집탐방",
		"Occasion_키덜트" :"키덜트",
		"Occasion_데이트" :"데이트",
		"Occasion_공부" :"공부",
		"Occasion_디저트" :"디저트",
		"Occasion_영화" :"영화",
		"Occasion_뷰티" :"뷰티",
		"Occasion_끼니" :"끼니",
		"Occasion_음주" :"음주",
		"Occasion_경조사" :"경조사",
		"Occasion_쇼핑" :"쇼핑",
		"Occasion_여행" :"여행",

		"With_with유아" :"유아",
		"With_with친구" :"친구",
		"With_with가족" :"가족",
		"With_with어른" :"어른",

		"Season_spring" :"봄",
		"Season_summer" :"여름",
		"Season_autumn" :"가을",
		"Season_winter" :"겨울",
		"isWeekend_weekday" :"주중",
		"isWeekend_weekend" :"주말",
		"isHoliday_휴일":"휴일",
		"isAnniversary_기념일" :"기념일",
		"maen_morning" :"아침",
		"maen_afternoon" :"오후",
		"maen_evening" :"저녁",
		"maen_night" :"밤",
	};
	if (words[param] == undefined) {
		return param;
	}
	return words[param];
}

function count_by_time(data){
	var data_count = {};
	for (var d in data){
		var _date = data[d]['date'].substring(0, 7);
		if (data_count[_date]== undefined){
			data_count[_date] = 1;
		} else {
			data_count[_date] += 1;
		}
	}
	return data_count;
}
function count_activity_by_time(data){
	var data_count = {};
	for (var d in data){
		var _date = data[d]['date'].substring(0, 7);
		if (data_count[_date]== undefined){
			data_count[_date] = {};
		} else {
			for (var p in data[d]['activities']){
				var act = data[d]['activities'][p];
				if(data_count[_date][act]== undefined){
					data_count[_date][act] = 1;
				} else {

				data_count[_date][act] +=1;}
			}
		}
	}
	return data_count;
}


function appendDict(work, living, leisure){
	var data= {};
	for (var a in work){
		if (data[a] == undefined ){
			data[a] = {};
		}
		data[a]["work"] = work[a];
	}
	for (var a in living){
		if (data[a] == undefined ){
			data[a] = {};
		}
		data[a]["living"] = living[a];
	}
	for (var a in leisure){
		if (data[a] == undefined ){
			data[a] = {};
		}
		data[a]["leisure"] = leisure[a];
	}
	return data;
}
