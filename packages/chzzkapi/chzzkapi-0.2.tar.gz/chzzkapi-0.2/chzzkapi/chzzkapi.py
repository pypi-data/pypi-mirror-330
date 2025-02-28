import requests

# 기존의 _get_channel_data 함수
def _get_channel_data(channel_id):
    url = f"https://api.chzzk.naver.com/service/v1/channels/{channel_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
        data = response.json()

        if 'content' not in data:  # 'content' 키가 없으면 반환
            return None

        return data['content']  # 'content' 안에 실제 데이터가 있음
    except requests.exceptions.RequestException as e:
        return None

# 개별 정보 반환 함수들
def channel_id(channel_id):
    content = _get_channel_data(channel_id)
    return content.get("channelId") if content else None

def channel_name(channel_id):
    content = _get_channel_data(channel_id)
    return content.get("channelName") if content else None

def channel_image_url(channel_id):
    content = _get_channel_data(channel_id)
    return content.get("channelImageUrl") if content else None

def verified_mark(channel_id):
    content = _get_channel_data(channel_id)
    return content.get("verifiedMark") if content else None

def channel_type(channel_id):
    content = _get_channel_data(channel_id)
    return content.get("channelType") if content else None

def channel_description(channel_id):
    content = _get_channel_data(channel_id)
    return content.get("channelDescription") if content else None

def follower_count(channel_id):
    content = _get_channel_data(channel_id)
    return content.get("followerCount") if content else None

def connect_cafe(channel_id):
    url = f"https://api.chzzk.naver.com/service/v1/channels/{channel_id}/cafe-connection"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
        data = response.json()

        if 'content' in data and data['content'] and 'name' in data['content']:
            cafe_name = data['content'].get('name')
            if cafe_name:
                return cafe_name
            else:
                return "연결된 카페가 없습니다."
        else:
            return "연결된 카페가 없습니다."
    except requests.exceptions.RequestException as e:
        return "연결된 카페가 없습니다."
