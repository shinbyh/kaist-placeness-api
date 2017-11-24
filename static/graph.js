

function chart(work_data, leisure_data, living_data){
	AmCharts.makeChart("chartdiv", {
		"type": "serial",
		"theme": "light",
		"legend": {
			"horizontalGap": 10,
			"maxColumns": 1,
			"position": "right",
			"useGraphSettings": true,
			"markerSize": 10
		},
		"dataProvider": [{
			"act": "Work",
			"business" : work_data['business'],
			"education" : work_data['education'],
			"legal" : work_data['legal']
		}, {
			"act": "Living",
			"relaxation" : living_data['relaxation'],
			"chores" : living_data['chores'],
			"housing" : living_data['housing'],
			"dining" : living_data['dining'],
			"health" : living_data['health'],
			"childcare" : living_data['childcare'],
			"religion" : living_data['religion']
		}, {
			"act": "Leisure",
			"fashionandbeauty" : leisure_data['fashionandbeauty'],
			"traveling" : leisure_data['traveling'],
			"outdoor" : leisure_data['outdoor'],
			"social" : leisure_data['social'],
			"entertainment" : leisure_data['entertainment'],
			"artandculture" : leisure_data['artandculture']
		}],
		"valueAxes": [{
			"stackType": "regular",
			"axisAlpha": 0.3,
			"gridAlpha": 0
		}],
		"graphs": [{
			"balloonText": "<b>[[title]]</b><br><span style='font-size:14px'> <b>[[value]]</b></span>",
			"fillAlphas": 0.8,
			"labelText": "[[title]] : [[value]]",
			"lineAlpha": 0.3,
			"title": "fashionandbeauty",
			"type": "column",
			"color": "#000000",
			"valueField": "fashionandbeauty"
		}, {
			"balloonText": "<b>[[title]]</b><br><span style='font-size:14px'> <b>[[value]]</b></span>",
			"fillAlphas": 0.8,
			"labelText": "[[title]] : [[value]]",
			"lineAlpha": 0.3,
			"title": "business",
			"type": "column",
			"color": "#000000",
			"valueField": "business"
		}, {
			"balloonText": "<b>[[title]]</b><br><span style='font-size:14px'> <b>[[value]]</b></span>",
			"fillAlphas": 0.8,
			"labelText": "[[title]] : [[value]]",
			"lineAlpha": 0.3,
			"title": "social",
			"type": "column",
			"color": "#000000",
			"valueField": "social"
		}, {
			"balloonText": "<b>[[title]]</b><br><span style='font-size:14px'> <b>[[value]]</b></span>",
			"fillAlphas": 0.8,
			"labelText": "[[title]] : [[value]]",
			"lineAlpha": 0.3,
			"title": "relaxation",
			"type": "column",
			"color": "#000000",
			"valueField": "relaxation"
		}, {
			"balloontext": "<b>[[title]]</b><br><span style='font-size:14px'> <b>[[value]]</b></span>",
			"fillalphas": 0.8,
			"labelText": "[[title]] : [[value]]",
			"linealpha": 0.3,
			"title": "traveling",
			"type": "column",
			"color": "#000000",
			"valuefield": "traveling"
		}, {
			"balloontext": "<b>[[title]]</b><br><span style='font-size:14px'> <b>[[value]]</b></span>",
			"fillalphas": 0.8,
			"labelText": "[[title]] : [[value]]",
			"linealpha": 0.3,
			"title": "education",
			"type": "column",
			"color": "#000000",
			"valuefield": "education"
		}, {
			"balloonText": "<b>[[title]]</b><br><span style='font-size:14px'> <b>[[value]]</b></span>",
			"fillAlphas": 0.8,
			"labelText": "[[title]] : [[value]]",
			"lineAlpha": 0.3,
			"title": "chores",
			"type": "column",
			"color": "#000000",
			"valueField": "chores"
		}, {
			"balloonText": "<b>[[title]]</b><br><span style='font-size:14px'> <b>[[value]]</b></span>",
			"fillAlphas": 0.8,
			"labelText": "[[title]] : [[value]]",
			"labelText": "[[value]]",
			"lineAlpha": 0.3,
			"title": "housing",
			"type": "column",
			"color": "#000000",
			"valueField": "housing"
		}, {
			"balloonText": "<b>[[title]]</b><br><span style='font-size:14px'> <b>[[value]]</b></span>",
			"fillAlphas": 0.8,
			"labelText": "[[title]] : [[value]]",
			"lineAlpha": 0.3,
			"title": "outdoor",
			"type": "column",
			"color": "#000000",
			"valueField": "outdoor"
		}, {
			"balloonText": "<b>[[title]]</b><br><span style='font-size:14px'> <b>[[value]]</b></span>",
			"fillAlphas": 0.8,
			"labelText": "[[title]] : [[value]]",
			"lineAlpha": 0.3,
			"title": "dining",
			"type": "column",
			"color": "#000000",
			"valueField": "dining"
		}, {
			"balloonText": "<b>[[title]]</b><br><span style='font-size:14px'> <b>[[value]]</b></span>",
			"fillAlphas": 0.8,
			"labelText": "[[title]] : [[value]]",
			"lineAlpha": 0.3,
			"title": "childcare",
			"type": "column",
			"color": "#000000",
			"valueField": "childcare"
		}, {
			"balloonText": "<b>[[title]]</b><br><span style='font-size:14px'> <b>[[value]]</b></span>",
			"fillAlphas": 0.8,
			"labelText": "[[title]] : [[value]]",
			"lineAlpha": 0.3,
			"title": "artandculture",
			"type": "column",
			"color": "#000000",
			"valueField": "artandculture"
		}, {
			"balloonText": "<b>[[title]]</b><br><span style='font-size:14px'> <b>[[value]]</b></span>",
			"fillAlphas": 0.8,
			"labelText": "[[title]] : [[value]]",
			"lineAlpha": 0.3,
			"title": "entertainment",
			"type": "column",
			"color": "#000000",
			"valueField": "entertainment"
		}, {
			"balloonText": "<b>[[title]]</b><br><span style='font-size:14px'> <b>[[value]]</b></span>",
			"fillAlphas": 0.8,
			"labelText": "[[title]] : [[value]]",
			"lineAlpha": 0.3,
			"title": "religion",
			"type": "column",
			"color": "#000000",
			"valueField": "religion"
		}, {
			"balloonText": "<b>[[title]]</b><br><span style='font-size:14px'> <b>[[value]]</b></span>",
			"fillAlphas": 0.8,
			"labelText": "[[title]] : [[value]]",
			"lineAlpha": 0.3,
			"title": "health",
			"type": "column",
			"color": "#000000",
			"valueField": "health"
		}, {
			"balloonText": "<b>[[title]]</b><br><span style='font-size:14px'> <b>[[value]]</b></span>",
			"fillAlphas": 0.8,
			"labelText": "[[title]] : [[value]]",
			"lineAlpha": 0.3,
			"title": "legal",
			"type": "column",
			"color": "#000000",
			"valueField": "legal"
		}],
		"categoryField": "act",
		"categoryAxis": {
			"gridPosition": "start",
			"axisAlpha": 0,
			"gridAlpha": 0,
			"position": "left"
		},
		"export": {
			"enabled": true
		 }

	});
}
function data_refined(data) {
	var data_ = [];
	for (var d in data){
		data[d]['date'] = d;
		data_.push(data[d]);
	}
	return data_.sort(function (a,b) {
		if (a.date < b.date){
			return -1;
		} else if (a.date > b.date){
			return 1;
		} else {
			return 0;
		}
	});
}

function time_graph(data){
	var data_ = data_refined(data);
	AmCharts.makeChart("time_graph", {
		"type": "serial",
		"theme": "light",
		"legend": {
			"useGraphSettings": true
		},
		"dataProvider": data_,
		"valueAxes": [{
			"integersOnly": true,
			"axisAlpha": 0,
			"dashLength": 5,
			"gridCount": 10,
			"position": "left",
		}],
		"startDuration": 0.5,
		"graphs": [{
			"balloonText": "work : [[value]]",
			"bullet": "round",
			"title": "Work",
			"valueField": "work",
			"fillAlphas": 0
		}, {
			"balloonText": "living : [[value]]",
			"bullet": "round",
			"title": "Living",
			"valueField": "living",
			"fillAlphas": 0
		}, {
			"balloonText": "leisure: [[value]]",
			"bullet": "round",
			"title": "Leisure",
			"valueField": "leisure",
			"fillAlphas": 0
		}],
		"chartCursor": {
			"cursorAlpha": 0,
			"zoomable": false
		},
		"categoryField": "date",
		"categoryAxis": {
			"gridPosition": "start",
			"axisAlpha": 0,
			"fillAlpha": 0.05,
			"fillColor": "#000000",
			"gridAlpha": 0,
			"position": "top"
		},
		"export": {
			"enabled": true,
			"position": "bottom-right"
		 }
	});
}
function time_work_graph(data){
	var data_ = data_refined(data);
	var act_list = ['business', 'education', 'legal'];
	var graph = [];
	for (var d in act_list){
		graph.push({"balloonText": "[[title]] : [[value]]", "bullet": "round", "title": act_list[d], "valueField":act_list[d],  "fillAlphas": 0});
	}
	AmCharts.makeChart("time_work_graph", {
		"type": "serial",
		"theme": "light",
		"legend": {
			"useGraphSettings": true
		},
		"dataProvider": data_,
		"valueAxes": [{
			"integersOnly": true,
			"axisAlpha": 0,
			"dashLength": 5,
			"gridCount": 10,
			"position": "left",
		}],
		"startDuration": 0.5,
		"graphs": graph,
		"chartCursor": {
			"cursorAlpha": 0,
			"zoomable": false
		},
		"categoryField": "date",
		"categoryAxis": {
			"gridPosition": "start",
			"axisAlpha": 0,
			"fillAlpha": 0.05,
			"fillColor": "#000000",
			"gridAlpha": 0,
			"position": "top"
		},
		"export": {
			"enabled": true,
			"position": "bottom-right"
		 }
	});
}
function time_living_graph(data){
	var data_ = data_refined(data);
	var graph = [];
	var act_list = ['relaxation', 'religion', 'chores', 'dining', 'childcare', 'health'];
	for (var d in act_list){
		graph.push({"balloonText": "[[title]] : [[value]]", "bullet": "round", "title": act_list[d], "valueField":act_list[d],  "fillAlphas": 0});
	}
	AmCharts.makeChart("time_living_graph", {
		"type": "serial",
		"theme": "light",
		"legend": {
			"useGraphSettings": true
		},
		"dataProvider": data_,
		"valueAxes": [{
			"integersOnly": true,
			"axisAlpha": 0,
			"dashLength": 5,
			"gridCount": 10,
			"position": "left",
		}],
		"startDuration": 0.5,
		"graphs": graph,
		"chartCursor": {
			"cursorAlpha": 0,
			"zoomable": false
		},
		"categoryField": "date",
		"categoryAxis": {
			"gridPosition": "start",
			"axisAlpha": 0,
			"fillAlpha": 0.05,
			"fillColor": "#000000",
			"gridAlpha": 0,
			"position": "top"
		},
		"export": {
			"enabled": true,
			"position": "bottom-right"
		 }
	});
}
function time_leisure_graph(data){
	var data_ = data_refined(data);
	var graph = [];
	var act_list = ['artandculture', 'entertainment', 'fashionandbeauty', 'outdoor', 'social', 'traveling'];
	for (var d in act_list){
		graph.push({"balloonText": "[[title]] : [[value]]", "bullet": "round", "title": act_list[d], "valueField":act_list[d],  "fillAlphas": 0});
	}
	AmCharts.makeChart("time_leisure_graph", {
		"type": "serial",
		"theme": "light",
		"legend": {
			"useGraphSettings": true
		},
		"dataProvider": data_,
		"valueAxes": [{
			"integersOnly": true,
			"axisAlpha": 0,
			"dashLength": 5,
			"gridCount": 10,
			"position": "left",
		}],
		"startDuration": 0.5,
		"graphs": graph,
		"chartCursor": {
			"cursorAlpha": 0,
			"zoomable": false
		},
		"categoryField": "date",
		"categoryAxis": {
			"gridPosition": "start",
			"axisAlpha": 0,
			"fillAlpha": 0.05,
			"fillColor": "#000000",
			"gridAlpha": 0,
			"position": "top"
		},
		"export": {
			"enabled": true,
			"position": "bottom-right"
		 }
	});
}
