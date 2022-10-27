from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import configparser, json, os, requests
from imageContrastCorrection import imageContrastCorrect
from requests_toolbelt.multipart.encoder import MultipartEncoder

config = {}
with open('./config/config.json', 'r') as f:
  config = json.load(f)

app = Flask(__name__)

# 일반적인 라우트 방식입니다.
@app.route('/receipt', methods=['POST'])
def processing():
  if not request.files['file']:
    return 'No image served.'

  image_file = request.files['file']
  path = './origin/'+image_file.filename
  image_file.save(path)
  new_path = imageContrastCorrect(path)
  multipart_form_data = MultipartEncoder(
    fields={
      'file':(os.path.basename(new_path),open(new_path,'rb')),
      'message': '{\
        "images": [{"format": "jpeg", "name": "sample"}],\
        "requestId": "capstone", "version": "V2", "timestamp": 0\
      }'
    }
  )

  targetParceData = requests.post(
    config['CLOVA_URI'],
    headers={
      'X-OCR-SECRET': config['X_OCR_SECRET'],
      'Content-Type':multipart_form_data.content_type
    },
    data=multipart_form_data
  )
  
  return jsonify(targetParceData.json())

app.run(host="localhost",debug=True)

#     //2. CLOVA 전송
#     const targetParceData = await axios
#       .post(api_url, form, {
#         headers: {
#           ...form.getHeaders(),
#           'X-OCR-SECRET': process.env.X_OCR_SECRET,
#         },
#       })

#     let ocr_result = {
#       items: []
#     }

#     let target_store = {}

#     let clovaCVData = targetParceData.data.images[0].receipt.result

#     let { paymentInfo, storeInfo, subResults, totalPrice } = clovaCVData

#     if (paymentInfo) {
#       ocr_result.payDate = Object.assign({}, (paymentInfo?.date?.formatted || {}), (paymentInfo?.time?.formatted || {}))
#     }
#     else {
#       ocr_result.payDate = null
#     }

#     ocr_result.store = {
#       name: storeInfo.name.formatted.value || storeInfo.subName.formatted.value,
#       addresses: storeInfo.addresses[0].text,
#       tel: '',
#       category:''
#     }

#     fs.writeFileSync(__dirname+`/../data/${Date.now().toString()}_${ocr_result.store.name}.json`, JSON.stringify(clovaCVData))
#     if (storeInfo.tel) {
#       ocr_result.store.tel = storeInfo.tel[0].formatted.value
#     }

#     ocr_result.store.name = ocr_result.store.name.replace('(주)', '')

#     if (subResults.length != 0) {
#       subResults[0].items.forEach(r => {
#         let name = r.name?.text || '정보 없음'
#         let count =  parseInt(r.count?.formatted?.value || r.count?.text || '1')
#         let price =  parseInt(r.price?.price?.formatted?.value || r.price?.price?.text || '0')
#         count=isNaN(count)?1:count
#         price=isNaN(price)?1:price
  
#         ocr_result.items.push({name, count, price})
#       })
#     }

#     ocr_result.totalPrice = parseInt(totalPrice?.price?.formatted.value||'0')

#     //1. store.address로 x, y 구하기
#     let result = await axios.get('https://dapi.kakao.com/v2/local/search/address.json', {
#       headers: {
#         Authorization: process.env.KAKAO_API_KEY
#       },
#       params: {
#         query: ocr_result.store.addresses
#       }
#     })

#     if(!result.data.documents.legnth){//결과값이 존재하지 않는다면
#       var regex=/(([가-힣A-Za-z·\d~\-\.]{2,}(로|길).[\d]+)|([가-힣A-Za-z·\d~\-\.]+(읍|동)\s)[\d]+)/
#       result = await axios.get('https://dapi.kakao.com/v2/local/search/address.json', {
#       headers: {
#         Authorization: process.env.KAKAO_API_KEY
#       },
#       params: {
#         query: ocr_result.store.addresses.match(regex)[1]
#       }
#     })
#     }
#     console.log()
#     //2. x,y, keyword()
#     let { x, y } = result.data.documents[0].address
#     ocr_result.store.cord={ x, y }
#     result = await axios.get('https://dapi.kakao.com/v2/local/search/keyword.json', {
#       headers: {
#         Authorization: process.env.KAKAO_API_KEY
#       },
#       params: {
#         query: ocr_result.store.name,
#         x,
#         y,
#         radius: 500, // 200m 내외로 검색
#         sort: 'accuracy'
#       }
#     })

#     console.log(result.data)

#     if (result.data.documents.length != 0) { // keyword 검색 결과가 존재하지 않으면 넘기기
#       result.data.documents.forEach(r => {
#         if (r.phone.replace(/\-/g, '') == ocr_result.store.tel) {
#           target_store = Object.assign({}, target_store, r)
#         }
#       })

#       if (Object.keys(target_store).length == 0) {
#         target_store = result.data.documents[0]
#       }

#       ocr_result.store.category = target_store?.category_group_name || ''
#       ocr_result.store.name = target_store?.place_name || ocr_result.store.name
#       ocr_result.store.addresses = target_store?.road_address_name || target_store?.address_name
#     }
    
#     console.log(ocr_result)

#     fs.unlinkSync(__dirname + "/../" + req.file.path)
#     return res.status(StatusCodes.OK).json({
#       data : ocr_result
#     })

#     //3. file 삭제
#   } catch (error) {
#     console.log(error)
#     fs.unlinkSync(__dirname + "/../" + req.file.path)
#     throw new Error('서버 내부 오류 발생, 다시 시도해주세요.')
#   }