import chzzkapi as chzzk

channel_id_value = "Chzzk_Channel_ID"

# 필요한 정보들만 출력
print("Channel ID:", chzzk.channel_id(channel_id_value))
print("Channel Name:", chzzk.channel_name(channel_id_value))
print("Channel Image URL:", chzzk.channel_image_url(channel_id_value))
print("Verified Mark:", chzzk.verified_mark(channel_id_value))
print("Channel Type:", chzzk.channel_type(channel_id_value))
print("Channel Description:", chzzk.channel_description(channel_id_value))
print("Follower Count:", chzzk.follower_count(channel_id_value))
print("Connect Cafe:", chzzk.connect_cafe(channel_id_value))