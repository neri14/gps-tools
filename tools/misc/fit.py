from garmin_fit_sdk import Decoder, Stream

def get_fit_data(path):
    stream = Stream.from_file(path)
    decoder = Decoder(stream)
    messages,_ = decoder.read()

    data = {}

    for msg in messages['record_mesgs']:
        frame = {}

        if 'timestamp' not in msg:
            continue #ignore point if missing timestamp

        ts = msg['timestamp']

        for k,v in msg.items():
            match k:
                case 'latitude':
                    frame[k] = v / 11930465  # magic value to convert to degrees
                case 'longitude':
                    frame[k] = v / 11930465  # magic value to convert to degrees
                case 'speed':
                    frame[k] = v * 3.6   # convert speed to km/h
                case _:
                    frame[k] = v

        data[ts] = frame

    return data
