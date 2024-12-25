from flask import jsonify, request
from . import api
from models import Topic, SessionLocal

@api.route('/api/topics', methods=['GET'])
def get_topics():
    """Get all topics"""
    try:
        with SessionLocal() as db:
            topics = db.query(Topic).all()
            return jsonify([{
                'name': topic.name,
                'format': topic.format,
                'schema': topic.schema
            } for topic in topics])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/api/topics', methods=['POST'])
def save_topics():
    """Save topics"""
    try:
        data = request.json
        topics = data.get('topics', [])
        
        with SessionLocal() as db:
            # Clear existing topics
            db.query(Topic).delete()
            
            # Add new topics
            for topic in topics:
                db_topic = Topic(
                    name=topic['name'],
                    format=topic['format'],
                    schema=topic.get('schema')
                )
                db.add(db_topic)
            
            db.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500