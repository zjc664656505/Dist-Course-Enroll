# Frontend API

## GET insert/delete
### insert/delete one record
params

	classId
	student   #name of student

response

	{"error": "reason"}        If something go wrong
	{"success": "success"}     If successful

## GET records
### get all the registration info
response

	[
		[classId, studentname],
		[1, "john"],
		...
	]

# Backend API

## GET insert/delete
### insert/delete one record
params

	classId
	student   #name of student
## GET list      
### list info of class in range [low, high)
params

	low    #lowest classid to fetch
	high

json response

	{
	  "low" : {
		"max": "30", 
		"students": ["john", "tom"]
	  },
	  "low+1" : {...},
	  ...
	  "high-1" : {...},
	}