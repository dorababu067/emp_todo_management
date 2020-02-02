import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyDEDszA-TxMHw4LRPqez66qptQQ7xwtMLA",
    "authDomain": "emp-todo-management-system.firebaseapp.com",
    "databaseURL": "https://emp-todo-management-system.firebaseio.com",
    "projectId": "emp-todo-management-system",
    "storageBucket": "emp-todo-management-system.appspot.com",
    "messagingSenderId": "650841791756",
    "appId": "1:650841791756:web:5b4c09b8b6f223dea1bd29",
    "measurementId": "G-R3KSXQKJ04"
  }

emp_todo = pyrebase.initialize_app(firebaseConfig)

fire_auth = emp_todo.auth()
fire_db = emp_todo.database()


# Firebase CRUD Operations

def create_emp(username = None, email = None, password = None):
  user = fire_auth.create_user_with_email_and_password(email, password)
  user_data = {
        "username" : username,
        "email"    : email
      }
  fire_db.child("users").child(user["localId"]).child("profile").set(user_data)


#create the task and storing into the firebase db
def create_task(uid = None, title = None, description = None, spent_time = None):
  task_data = {
        "title" : title,
        "description" : description,
        "spent_time"   : spent_time
      }
  fire_db.child("users").child(uid).child("tasks").push(task_data)

#getting the tasks form the firebase db 
def get_tasks(uid = None):
  tasks = []
  try:
    user_task_ids = fire_db.child("users").child(uid).child("tasks").get().val()
    for task_id in user_task_ids:
      task = fire_db.child("users").child(uid).child("tasks").child(task_id).get().val()
      task.update({"ts_id" : task_id })
      tasks.append(task)
    return tasks
  except:
    return tasks

def get_task_data(uid = None, task_id = None):
    fm_data = dict()
    ts_data = fire_db.child("users").child(uid).child("tasks").child(task_id).get().val()
    for key in ts_data.keys():
      fm_data[key] = ts_data[key]
    return fm_data

def get_task_data_update(uid = None, task_id = None, title = None, description = None, spent_time = None):
  up_fm_data = {
    "title" : title,
    "description" : description,
    "spent_time" : spent_time
  }
  fire_db.child("users").child(uid).child("tasks").child(task_id).update(up_fm_data)

def check_user_login_or_not():
  user = {}
  try:
    uid = request.session['uid']
    username = fire_db.child("users").child(uid).child("profile").child("username").get().val()
    user["login"] = True,
    user["username"] = username
    return user
  except:
    return user
