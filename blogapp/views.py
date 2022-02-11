from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import *


class PostView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        try:
            query = Post.objects.all()
            serialize = PostSerializer(query, many=True)
            data = []
            for post in serialize.data:
                my_like = Like.objects.filter(post_id=post["id"]).filter(user=request.user).first()
                if my_like:
                    post["my_like"] = my_like.like
                else:
                    post["my_like"] = False
                post_like = Like.objects.filter(post_id=post["id"]).filter(like=True).count()
                post["total_like"] = post_like
                comment_query = Comment.objects.filter(post_id=post["id"]).order_by('-id')
                comment_serializer = CommentSerializer(comment_query, many=True)
                post["comment"] = comment_serializer.data
                reply_data = []
                for comment in comment_serializer.data:
                    reply_query = Reply.objects.filter(comment=comment["id"])
                    reply_serializer = ReplySerializer(reply_query, many=True)
                    comment["reply"] = reply_serializer.data
                    reply_data.append(comment)
                data.append(post)
            response_message = {
                "success": True,
                "message": "",
                "data": serialize.data,
                "error": "",
                "error_code": 200}
        except Exception as e:
            response_message = {
                "success": False,
                "message": str(e),
                "data": "",
                "error": "",
                "error_code": 400}
        return Response(response_message)


class CategoryView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, response):
        try:
            category_obj = Category.objects.all()
            serializer = CategorySerializer(category_obj, many=True)
            response_message = {
                "success": True,
                "message": "",
                "data": serializer.data,
                "error": "",
                "error_code": 200}
        except Exception as e:
            response_message = {
                "success": False,
                "message": str(e),
                "data": "",
                "error": e,
                "error_code": 400}

        return Response(response_message)


class AddLike(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            user = request.user
            post_id = request.data['id']
            post_obj = Post.objects.get(id=post_id)
            like_obj = Like.objects.filter(post=post_obj).filter(user=user).first()
            if like_obj:
                old_like = like_obj.like
                like_obj.like = not old_like
                like_obj.save()
            else:
                Like.objects.create(
                    user=user,
                    post=post_obj,
                    like=True
                )
            response_message = {
                "success": True,
                "message": "",
                "data": "Status has been changed",
                "error": "",
                "error_code": 200}
        except Exception as e:
            response_message = {
                "success": False,
                "message": str(e),
                "data": "",
                "error": "",
                "error_code": 400}

        return Response(response_message)


class AddComment(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            user = request.user
            post_id = request.data['id']
            post_obj = Post.objects.get(id=post_id)
            Comment.objects.create(
                user_id=user,
                post_id=post_obj,
                comment=request.data["comment"]
            )
            response_message = {
                "success": True,
                "message": "",
                "data": "Status has been changed",
                "error": "",
                "error_code": 200}
        except Exception as e:
            response_message = {
                "success": False,
                "message": str(e),
                "data": "",
                "error": "",
                "error_code": 400}

        return Response(response_message)


class ReplyView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, response):

        try:
            user = response.user
            comment_id = response.data["id"]
            comment_obj = Comment.objects.get(id=comment_id)
            Reply.objects.create(
                user=user,
                comment=comment_obj,
                reply=response.data["reply"]
            )
            response_message = {
                "success": True,
                "message": "",
                "data": "Status has been changed",
                "error": "",
                "error_code": 200}
        except Exception as e:
            response_message = {
                "success": False,
                "message": str(e),
                "data": "",
                "error": "",
                "error_code": 400}

        return Response(response_message)


class Registration(APIView):
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                print(serializer.data)
            response_message = {
                "success": True,
                "message": "",
                "data": "User has been created successfully",
                "error": "",
                "error_code": 200}
        except Exception as e:
            response_message = {
                "success": False,
                "message": str(e),
                "data": "",
                "error": "",
                "error_code": 400}

        return Response(response_message)
