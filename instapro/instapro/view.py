from django.http import JsonResponse
from instagram_private_api import Client

def get_profile(request):
    # Retrieve the username from the API request
    username = request.GET.get('fab_boy_abik')

    # Provide your Instagram username and password
    username = 'fab_boy_abik'
    password = '5SPPibFbgO'

    # Authenticate with Instagram
    api = Client(username, password)

    try:
        # Retrieve the user's profile by username
        user_id = api.username_info(username)['user']['pk']
        user_info = api.user_info(user_id)

        # Extract and return the profile details
        profile_details = user_info['user']
        response = {
            'username': profile_details['username'],
            'full_name': profile_details['full_name'],
            'bio': profile_details['biography'],
            'followers': profile_details['follower_count'],
            'following': profile_details['following_count']
        }
       # Retrieve the user's stories
        stories = api.user_reel_media(user_id)
        story_urls = []
        for item in stories['items']:
            if 'image_versions2' in item and 'candidates' in item['image_versions2']:
                url = item['image_versions2']['candidates'][0]['url']
                story_urls.append(url)
            elif 'video_versions' in item:
                url = item['video_versions'][0]['url']
                story_urls.append(url)

        response['stories'] = story_urls
        print(JsonResponse(response))
        return JsonResponse(response)

    except Exception as e:
        error_message = str(e)
        response = {'error': error_message}
        return JsonResponse(response, status=400)
