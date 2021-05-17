from flask import Flask, request, jsonify, render_template
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

# กำหนด description อธิบายว่าชื่ออะไร title อะไร
api = Api(app, version='1.0', title='Hiring API',
            description='A simple Hiring API',
            )
# กำหนด namespace
ns = api.namespace('hiring', description='Hiring operations')

# data model
employee_model = api.model('Employee', {
    'id': fields.Integer(readonly=True, desclearcription='The task unique identifier'),
    'name': fields.String(required=True, description='Name'),
    'experience': fields.Integer(required=True, description='Experience'),
    'test_score': fields.Integer(required=True, description='Test Score'),
    'interview_score': fields.Integer(required=True, description='Interview Score'),
    'salary': fields.Integer(required=True, description='Salary')
})

class TaskEmployee(object):
    # constructer ทำงานเมื่อobjectถูกสร้าง
    def __init__(self):
        # self => member of class not function
        self.counter = 0
        self.employees = []

    def get(self, task_name):
        for t in self.employees:
            if t['name'] == task_name:
                return t
        api.abort(404, "Task {} doesn't exist".format(name))

    def create(self, data):
        task = {
            'id': self.counter + 1,
            'name': data['name'],
            'experience': data['experience'],
            'test_score': data['test_score'],
            'interview_score': data['interview_score'],
            'salary': data['salary'],
        }

        self.employees.append(task)
        self.counter = self.counter + 1
        return task

    def update(self, task_name, data):
        task = None
        for i, t in enumerate(self.employees):
            if t['name'] == task_name:
                task = {
                    'id': t['id'],
                    'name': data['name'],
                    'experience': data['experience'],
                    'test_score': data['test_score'],
                    'interview_score': data['interview_score'],
                    'salary': data['salary'],
                }
                self.employees[i] = task
        return task

    def delete(self, task_name):
        for i, t in enumerate(self.employees):
            if t['name'] == task_name:
                self.employees.remove(t)
                return

employee = TaskEmployee()
employee.create({'name': 'Kannicha', 'experience': 3, 'test_score': 10, 'interview_score': 8, 'salary': 5000})

@ns.route('/')
class EmployeeList(Resource):
    @ns.doc('list_employees')
    @ns.marshal_list_with(employee_model)
    def get(self):
        return employee.employees

    @ns.doc('create_task')
    @ns.expect(employee_model)
    @ns.marshal_with(employee_model, code=201)
    def post(self):
        return employee.create(api.payload), 201

@ns.route('/<task_name>')
@ns.response(404, 'Hiring not found')
@ns.param('task_name', 'The task identifier')
class Employee(Resource):
    @ns.doc('get_task')
    @ns.marshal_with(employee_model)
    def get(self, task_name):
        return employee.get(task_name)

    @ns.expect(employee_model)
    @ns.marshal_with(employee_model)
    def put(self, task_name):
        return employee.update(task_name, api.payload)
    
    @ns.doc('delete_task')
    @ns.response(204, 'Task deleted')
    def delete(self, task_name):
        employee.delete(task_name)
        return '', 204 

