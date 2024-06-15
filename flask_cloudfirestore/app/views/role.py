from flask.views import MethodView
from flask import request, jsonify

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
            
            db.session.add(new_item)
            
            db.session.commit()
            
            return jsonify({'message': 'Role created successfully'}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
