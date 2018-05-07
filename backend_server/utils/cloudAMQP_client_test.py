from cloudAMQP_client import CloudAMQPClient

# Use your own URL
CLOUDAMQP_URL = "amqp://spkrvejb:ezz3qAtWdO1JXuKVpaPV0CpwEjCO2Bhk@skunk.rmq.cloudamqp.com/spkrvejb"

TEST_QUEUE_NAME = 'test'

def test_basic():
    client = CloudAMQPClient(CLOUDAMQP_URL, TEST_QUEUE_NAME)

    sentMsg = {'test':'demo'}
    client.sendMessage(sentMsg)
    client.sleep(10)
    receivedMsg = client.getMessage()
    assert sentMsg == receivedMsg
    print 'test_basic passed!'

if __name__ == "__main__":
    test_basic()
