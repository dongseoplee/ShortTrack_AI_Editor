import torch
import glob
import os
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

target=0 #fall_down의 index
threshhold=0.7 #객체인식 임계 확률

# model = torch.hub.load("C:/Users/KIM YAECHAN/Desktop/졸업작품/content/yolov5", 'custom', path="C:/Users/KIM YAECHAN/Desktop/졸업작품/content/yolov5/runs/train/skate3/weights/best.pt", source='local')

# img = 'C:/Users/KIM YAECHAN/Desktop/졸업작품/val/AnyConv.com__8.jpg'
# test='C:/Users/KIM YAECHAN/Documents/GitHub/ShortTrack-AIEditor/ShortTrack/images/temp/frame0.png'
# video='C:/Users/KIM YAECHAN/Desktop/졸업작품/test_video.mp4'



def Object_detection(target='fall_down',threshhold=0.5):
    
    target_id_to_name = ['fall_down','skating','start', 'finish']
    target_name_to_id = {target_id_to_name[i]: i for i in range(len(target_id_to_name))}
    

    start_threshold=0.4
    finish_threshold=0.4

    #모델 파라미터 load
    model = torch.hub.load("yolov5", 'custom', path="./yolov5m_4object_best.pt", source='local')
    
    #객체를 index번호로 바꿈
    target=target_name_to_id[target]
    score=[]

    #frame path
    images=sorted(glob.glob('./images/temp/*'), key=os.path.getctime)

    for fname in images:

        results=model(fname)

        print(results.xyxyn)
        count_object=0 
        finish_flag=0
        start_flag=0

        for result in results.xyxyn[0]:
            #인식한 개체가 target일때
            if result[-1]==target:
                #인식 confidence가 threshold보다 높은지 확인
                if result[-2]>=threshhold:
                    print(fname)
                    print('Fall down Detected')
                    count_object+=1

            #start 인식
            elif result[-1]==2:
                #인식 confidence가 threshold보다 높은지 확인
                if result[-2]>=start_threshold:
                    print(fname)
                    print('Start Detected')
                    start_flag=1 

            #finish 인식
            elif result[-1]==3:
                #인식 confidence가 threshold보다 높은지 확인
                if result[-2]>=finish_threshold:
                    print(fname)
                    print('Finish Detected')
                    finish_flag=1

             

        if finish_flag==1:
            score.append(999)
        elif start_flag==1:
            score.append(999)
        else:
            score.append(count_object*50)
        #results.show()  
    print("objectDetectionScore:",score)
        
    return score

if __name__ == "__main__":
    # Object_detection()
    model = torch.hub.load("yolov5", 'custom', path="./yolov5m_4object_best.pt", source='local')
    # fname='testimage/KakaoTalk_20221202_173459150_10.png'
    fname='images/temp/frame148.png'
    results=model(fname)
    print(results.names)
    print(results.xyxyn)
    results.show()  