# Backend API
	Master  IP: renew each time
	Worker1 IP: renew each time
	Worker2 IP: renew each time
	
	Set up on nginx and Launch by gunicorn each time.
	
## Web access
### Login site and student register site
http://IP/login/

http://IP/register/
### Home site show the booking list
http://IP/home/
### Insert Course and remove booked course
Stay in http://IP/home/
### Logout
Todo
	
## API GET insert/delete
### insert one record
http://IP/api/add/**\<Student ID\>**/**\<Course ID\>**

### delete one record
http://IP/api/remove/**\<Student ID\>**/**\<Course ID\>**

## API GET info      
### list info of class in range 
http://IP/api/info

Json response
	
	{"34610": 
		{"ID": "CS202", 
		"name": "APPLIED CRYPTY", 
		"Instructor": "JARECKI", 
		"Max": 2,
		"student": ["Junchen", "Juncheng", "Yurun"]
		}, 
	
	"34625": { ... }, 
	...
	"34790": { ... }
	}
	
	
	
## Default Test Data 	

Course

	[34680, 'CS241', 'ADV COMPILER CONSTR', 'FRANZ', 4]
	[34700, 'CS260', 'FUND ALGORITHMS', 'HIRSCHBERG', 5]
	[34610, 'CS202', 'APPLIED CRYPTY', 'JARECKI', 2]
	[34660, 'CS230', 'DIST COMPUTER SYS', 'EL ZARKI', 4]
	[34720, 'CS263', 'ANALYSIS OF ALGRTHM', 'MIHAIL', 3]
	[34790, 'CS274A', 'PROB LEARNING', 'SMYTH', 6]
	[34625, 'CS211A', 'IMAGE UNDERSTANDING', 'MAJUMDER', 3]
	[34650, 'CS222', 'PRINCIPLS DATA MGMT', 'LI', 3]
	
Student

	[1, Yurun]
	[2, Junchen]
	[3, Juncheng]
	[4, Jason]
	[5, Ian]
	[6, Ryan]
	[7, Ali]
	[8, Daniel]
	[9, Iris]
	[10, Kevin]
	
Enrollment
	
	None
