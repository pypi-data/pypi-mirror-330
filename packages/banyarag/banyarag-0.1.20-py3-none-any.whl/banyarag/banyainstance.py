import os
import requests

import logging


# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from .file_uploader import upload_files_to_server

class BanyaInstance:
    def __init__(self, server_url="https://train.banya.ai", api_key=None, user_email=None, drive_path=None, bucket_timestamps=None):
        """
        BanyaInstance 초기화.

        :param server_url: 파일 업로드 및 학습 서버 URL
        :param api_key: 사용자의 API key
        :param user_email: 사용자의 이메일 주소
        """
        self.server_url = server_url
        self.api_key = api_key
        self.user_email = user_email
        self.drive_path = drive_path
        self.bucket_timestamps = bucket_timestamps
        self.chat_url = None

    def setDrivePath(self, drive_path):
        """
        드라이브 경로를 설정합니다.

        :param drive_path: 로컬 드라이브 경로
        :return: 경로 설정 성공 여부 (True/False)
        """
        try:
            if not os.path.isdir(drive_path):
                raise NotADirectoryError(f"Invalid drive path: {drive_path}")
            self.drive_path = drive_path
            logging.info(f"Drive path set to: {self.drive_path}")
            return True
        except Exception as e:
            logging.error(f"Failed to set drive path: {e}")
            return False

    def uploadAllFiles(self):
        """
        설정된 드라이브 경로 내 모든 파일을 서버로 업로드합니다.

        :return: 업로드 완료 타임스탬프 또는 False
        """
        try:
            if not self.drive_path:
                raise ValueError("Drive path is not set. Use setDrivePath() first.")

            # 드라이브 경로 내 모든 파일 목록 생성
            file_paths = []
            for root, dirs, files in os.walk(self.drive_path):
                for file in files:
                    file_paths.append(os.path.join(root, file))

            if not file_paths:
                logging.info("No files found in the drive path.")
                return False

            # API key와 사용자 이메일 검증
            if not self.api_key or not self.user_email:
                raise ValueError("API key and user email must be set for uploading files.")

            # 파일 업로드 수행 (업로드 URL 구성)
            upload_url = self.server_url + "/upload_user_files_lib/"
            response = upload_files_to_server(api_key=self.api_key, user_email=self.user_email,
                                              file_paths=file_paths, server_url=upload_url)

            if response is None:
                raise RuntimeError("Upload failed. No response from server.")

            # logging.info("Upload response:", response)


            # bucket_timestamps 업데이트
            if "bucket_timestamps" in response:
                self.bucket_timestamps = response["bucket_timestamps"]
                # logging.info(f"Updated bucket_timestamps: {self.bucket_timestamps}")


            return response
        except Exception as e:
            logging.error(f"Failed to upload files: {e}")
            return False

    def trainRAG(self, embedder=None, llm=None):
        """
        업로드된 데이터로 학습을 수행합니다.

        :param timestamp: 업로드 타임스탬프
        :param embedder: 임베더 모델 이름
        :param llm: LLM 모델 이름
        :return: 학습 완료 후 Chat URL 또는 False
        """

        
        
        try:
                        
            if not self.server_url:
                raise ValueError("Server URL is not set.")
            if not self.api_key:
                raise ValueError("API key is not set.")
            if not self.user_email:
                raise ValueError("User email is not set.")
            if not self.bucket_timestamps:
                raise ValueError("No bucket_timestamps found. Upload files first.")
            
            
            train_endpoint = f"{self.server_url}/llm/lib/trainer"
            payload = {
                "api_key": self.api_key,
                "user_email": self.user_email,
                "timestamp": self.bucket_timestamps,
                "embedder": embedder,
                "llm": llm,
            }

            response = requests.post(train_endpoint, data=payload)
            # logging.info(response.json())

            if response.status_code == 201:
                chat_url = response.json().get("data", {}).get("model_url", "")
                self.chat_url = chat_url
                logging.info(f"Training completed. Chat URL: {chat_url}")
                return chat_url
            else:
                raise RuntimeError(f"Training failed: {response.status_code} - {response.text}")
        except Exception as e:
            logging.error(f"Failed to train RAG: {e}")
            return False
        
        
        
    
    def getChatURL(self):
        """
        학습 완료 후 Chat URL을 반환합니다.

        :return: Chat URL
        """
        return self.chat_url

    def chat(self, params, chat_url=None):
        """
        Chat URL로부터 질의에 대한 답변을 반환합니다.

        :param : 질의 내용
        example
        parmas={
        "prompt":"한국어로 대답해줘",
        "message":"딸기재배방법",
        "model_name":"deepseek-r1:1.5b",
        "llmchat_user_api_key": "",//user's API 키
        "max_tokens": 2048, // 생성될 응답의 최대 토큰 수
        "temperature": 0.0,  // 모델의 창의성 수준
        "retriver_params":{
        "search_type": "similarity",
        "search_kwargs": {
                                "k": 2
                            },    
        "image_path":image_path
        }
        :param chat_url: Chat URL
        :return: 답변 문장
        """
        try:
            if not chat_url:
                chat_url = self.chat_url
            if not chat_url:
                raise ValueError("Chat URL is not set.")
            if not params:
                raise ValueError("params is empty.")

            chat_endpoint = f"{chat_url}"
            payload = params
            
            # if payload['image']:
        
            #     files = {
            #         "image":payload['image']
            #     }
            #     response = requests.post(chat_endpoint, data=payload, files=files)
                
            if payload.get('image'):  # 'image' 키가 있고 값이 존재하는지 확인
                files = {
                    "image": payload['image']  # 파일 객체로 전달
                }
                # payload에서 image 제거 (files로 별도 전달)
                payload_data = {k: v for k, v in payload.items() if k != 'image'}
                response = requests.post(chat_endpoint, data=payload_data, files=files)
                
            else:
                response = requests.post(chat_endpoint, json=payload)

            # 응답 확인
            response_data = response.json()
            return response_data
        except Exception as e:
            logging.error(f"Failed to chat: {e}")
            return False
