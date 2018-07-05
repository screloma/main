commands = {"неопределённый интеграл":
				{"function": "solve_integral(event, session)", 
				"message_type" :"attachment",
				"regex" :"неопредел[её]нный интеграл"},
			"расписание": 
				{"function": "get_schedule()",
				"message_type": "message",
				"regex": "где пара\??"},
			"футбол_вордфильтр":
				{"function":"pay_respects(event)",
				"message_type": "attachment",
				"regex": "фу+тбо+л|фу+тби+к|фу+тбо+льчи+к"}}