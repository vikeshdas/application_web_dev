from flask.views import MethodView
from flask import request, jsonify
from app.models import db
from app.models import Roles  

class RoleView(MethodView):
    """
        View class to handle Role related operations like creating role. Role can be like mobile,web .mobile means user can 
        access information using only mobile,or web or both.

    """
    def put(self):
        """
            Create new role.

            Args:
                request (HttpRequest): object of HttpRequest contains information of a role to save in database.

            Return:
                 Response(JsonResponse):return Jsonresponse either role created successfully or error.
        """
        try:
            data = request.get_json()

            new_item = Roles(name=data['name'],)
            duplicate_role = Roles.query.filter_by(name=data['name']).first()
            if duplicate_role:
                return jsonify({'error': "Role allready exist"}), 400
            db.session.add(new_item)
            
            db.session.commit()
            
            created_role = Roles.query.filter_by(name=data['name']).first()

            response_data = {'message': 'Role created successfully','role': {'id': created_role.id,'name': created_role.name}}

            return jsonify(response_data), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500