import os
import sqlite3
from flask import Flask,render_template,request,jsonify
 
from aws.ec2_manager import EC2Manager
from aws.s3_manager import S3Manager
from aws.iam_manager import IAMManager
from aws.cloudwatch_manager import CloudWatchManager
 
app=Flask(__name__)
 
DB_PATH=os.path.join('database','cloud.db')
 
def init_db():
    os.makedirs('database',exist_ok=True)
    os.makedirs('reports',exist_ok=True)
    os.makedirs('backups',exist_ok=True)
    conn=sqlite3.connect(DB_PATH)
    cursor=conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        action TEXT,
        target TEXT,
        status TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()
 
init_db()
 
def log_action(action,target,status):
    conn=sqlite3.connect(DB_PATH)
    cursor=conn.cursor()
    cursor.execute("INSERT INTO logs(action,target,status) VALUES (?, ?, ?)",(action,target,status))
    conn.commit()
    conn.close()
 
ec2=EC2Manager()
s3=S3Manager()
iam=IAMManager()
cw=CloudWatchManager()
 
@app.route('/')
def dashboard():
    conn=sqlite3.connect(DB_PATH)
    cursor=conn.cursor()
    cursor.execute("SELECT action,target,status,timestamp FROM logs ORDER BY timestamp DESC LIMIT 5")
    recent_logs=cursor.fetchall()
    conn.close()
    return render_template('dashboard.html',logs=recent_logs,active_page='overview')
 
@app.route('/ec2')
def ec2_page():
    return render_template('ec2.html',active_page='ec2')
 
@app.route('/s3')
def s3_page():
    return render_template('s3.html',active_page='s3')
 
@app.route('/iam')
def iam_page():
    return render_template('iam.html',active_page='iam')
 
@app.route('/logs')
def logs_page():
    conn=sqlite3.connect(DB_PATH)
    cursor=conn.cursor()
    cursor.execute("SELECT action,target,status,timestamp FROM logs ORDER BY timestamp DESC")
    all_logs=cursor.fetchall()
    conn.close()
    return render_template('logs.html',logs=all_logs,active_page='logs')
 
@app.route('/api/ec2/launch', methods=['POST'])
def api_launch_ec2():
    data=request.json or {}
    ami=data.get('ami', 'ami-0c55d159cbfafe1f0')
    res=ec2.launch_instance(ami)
    log_action("Launch EC2",res.get('instance_id','Failed'),res['status'])
    return jsonify(res)
 
@app.route('/api/ec2/stop',methods=['POST'])
def api_stop_ec2():
    instance_id=request.json.get('instance_id')
    res=ec2.stop_instance(instance_id)
    log_action("Stop EC2",instance_id,res['status'])
    return jsonify(res)
 
@app.route('/api/s3/create',methods=['POST'])
def api_create_s3():
    bucket_name=request.json.get('bucket_name')
    res=s3.create_bucket(bucket_name)
    log_action("Create S3 Bucket", bucket_name,res['status'])
    return jsonify(res)
 
@app.route('/api/iam/create',methods=['POST'])
def api_create_iam():
    username=request.json.get('username')
    res=iam.create_user(username)
    log_action("Create IAM User",username,res['status'])
    return jsonify(res)
 
@app.route('/api/monitor/cpu/<instance_id>',methods=['GET'])
def api_cpu(instance_id):
    return jsonify(cw.get_cpu_utilization(instance_id))
 
@app.route('/api/monitor/cost', methods=['GET'])
def api_cost():
    return jsonify(cw.get_cost_report())
 
@app.route('/api/logs/clear', methods=['POST'])
def clear_logs():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM logs")
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Audit logs cleared successfully."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
 
if __name__=='__main__':
    app.run(debug=True,port=5000)