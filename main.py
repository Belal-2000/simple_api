from flask import Flask
from flask_restful import Api , Resource , reqparse , abort , fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
api = Api(app)

db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(100) , nullable= False)
    likes = db.Column(db.Integer , nullable= False)
    views = db.Column(db.Integer , nullable= False)

    def __repr__(self):
        return f"Video(name = {self.name} , views = {self.views} , likes = {self.likes}"


vid_put_args = reqparse.RequestParser()
vid_put_args.add_argument('name' , type=str , help='name of the video' , required = True)
vid_put_args.add_argument('views' , type=int , help='views of the video' ,required = True)
vid_put_args.add_argument('likes' , type=int , help='likes of the video' , required = True)

vid_patch_args = reqparse.RequestParser()
vid_patch_args.add_argument('name' , type=str , help='name of the video')
vid_patch_args.add_argument('views' , type=int , help='views of the video')
vid_patch_args.add_argument('likes' , type=int , help='likes of the video')


resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}


class Video(Resource):
    @marshal_with(resource_fields)
    def get(self , vid_id):
        res = VideoModel.query.filter_by(id=vid_id).first()
        if not res:
            abort(404 , message= 'id not found ..')
        return res 

    @marshal_with(resource_fields)
    def put(self , vid_id):
        args = vid_put_args.parse_args()
        res = VideoModel.query.filter_by(id=vid_id).first()
        if res:
            abort(409 ,message= 'video id already taken .. ')
        video = VideoModel(id = vid_id, name=args['name'] , views = args['views'] , likes= args['likes'])
        db.session.add(video)
        db.session.commit()
        return video , 201

    @marshal_with(resource_fields)
    def patch(self , vid_id):
        args = vid_patch_args.parse_args()
        res = VideoModel.query.filter_by(id=vid_id).first()
        if not res :
            abort(404 , message= 'id not found ..')
        for k, v in args.items():
            if v:
                setattr(res, k, v)
        db.session.commit()
        return res , 201

    def delete(self , vid_id):
        pass

api.add_resource(Video , '/video/<int:vid_id>')

if __name__ == '__main__':
    app.run(debug=True)