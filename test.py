import replicate
import os



input = {
    "mask_type": "highlighted",
    "video_fps": 25,
    "input_video": "https://res.cloudinary.com/hkzbfes0n/video/upload/v1727031665/uploaded_videos/aojcuh3degxpxntslds4.mp4",
    "click_frames": "1",
    "output_video": True,
    "click_object_ids": "bee_1,bee_2,bee_3,bee_4,bee_5,bee_6,bee_7,bee_8",
    "click_coordinates": "[391,239],[178,320],[334,391],[185,446],[100,433],[461,499],[11,395],[9,461]"
}
output = replicate.run(
    "meta/sam-2-video:33432afdfc06a10da6b4018932893d39b0159f838b6d11dd1236dff85cc5ec1d",
    input=input
)
print(output)
    #=> "https://replicate.delivery/pbxt/iGyFurounuZkAFqPL7Rjq5bzL9WdE7AhUfdXmKlvEnroHTpJA/output_video.mp4"