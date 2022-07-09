import numpy as np
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc
import grpc
import tensorflow as tf

#YOLOv3, YOLOv4
def grpc_client_request_camera(img,
                        host='0.0.0.0',
                        port=8500,
                        img_name='input_1',
                        timeout=10):
    """
    Connect client with server by gRPC. The funciton by camera decode and server decode is YOLOv3 and YOLOv4
    """
    host = host.replace("http://", "").replace("https://", "")
    channel = grpc.insecure_channel("{}:{}".format(host, port))
    stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)

    # Create PredictRequest ProtoBuf from image data
    request = predict_pb2.PredictRequest()
    request.model_spec.name = "qr_detection_v4_tiny"
    # request.model_spec.name = "qr_detection_v3"
    # request.model_spec.name = "qr_detection_v4"

    request.model_spec.signature_name = "serving_default"
    # image

    request.inputs[img_name].CopyFrom(
        tf.contrib.util.make_tensor_proto(
            img,
            dtype=np.float32,
        )
    )

    # Call the TFServing Predict API
    result = stub.Predict(request, timeout=timeout)
    #yolov4_tiny
    lst_bbox = result.outputs['tf_op_layer_concat_14'].float_val
    #yolov4
    #lst_bbox = result.outputs['tf_op_layer_concat_18'].float_val
    #yolov3
    #lst_bbox = result.outputs['tf_op_layer_concat_10'].float_val
    return lst_bbox

def grpc_client_request_image(img,
                        host='0.0.0.0',
                        port=8500,
                        img_name='input_1',
                        timeout=10):
    """
    Connect client with server by gRPC. The funciton by image decode and server decode is YOLOv3 and YOLOv4
    """
    host = host.replace("http://", "").replace("https://", "")
    channel = grpc.insecure_channel("{}:{}".format(host, port))
    stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)

    # Create PredictRequest ProtoBuf from image data
    request = predict_pb2.PredictRequest()
    # request.model_spec.name = "qr_detection_v4_tiny"
    # request.model_spec.name = "qr_detection_v3"
    request.model_spec.name = "qr_detection_v4"

    request.model_spec.signature_name = "serving_default"
    # image

    request.inputs[img_name].CopyFrom(
        tf.contrib.util.make_tensor_proto(
            img,
            dtype=np.float32,
        )
    )

    # Call the TFServing Predict API
    result = stub.Predict(request, timeout=timeout)
    #yolov4_tiny
    #lst_bbox = result.outputs['tf_op_layer_concat_14'].float_val
    #yolov4
    lst_bbox = result.outputs['tf_op_layer_concat_18'].float_val
    #yolov3
    #lst_bbox = result.outputs['tf_op_layer_concat_10'].float_val
    return lst_bbox

#YOLOv5
def grpc_client_request_YOLOv5(img,
                        host='0.0.0.0',
                        port=8500,
                        img_name='x',
                        timeout=10):
    """
    Connect client with server by gRPC. The funciton by camera or image decode and server decode is YOLOv5
    """
    host = host.replace("http://", "").replace("https://", "")
    channel = grpc.insecure_channel("{}:{}".format(host, port))
    stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)
    # Create PredictRequest ProtoBuf from image data
    request = predict_pb2.PredictRequest()
    request.model_spec.name = "qr_detection_v5"
    request.model_spec.signature_name = "serving_default"
    request.inputs[img_name].CopyFrom(
        tf.contrib.util.make_tensor_proto(
            img,
            dtype=np.float32,
        )
    )
    # Call the TFServing Predict API
    result = stub.Predict(request, timeout=timeout)
    lst_bbox = result.outputs['output_0'].float_val

    return lst_bbox