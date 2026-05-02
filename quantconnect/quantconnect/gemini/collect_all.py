import subprocess
import os

ids = [
    "98cdeb9f114106c9a1f68c3253b58100", "8f2a709f6aa9f93908d30400a868089a", "debccd682ec16bd2e17360c0839759ff",
    "97d5c8012dd9939bc49af71a8e2b4506", "b53b1878cecf9c0e8be81bb3b3da34ae", "cbf134e91fad5fbecf5c81cab430f1ff",
    "ccd630e1bcc944fddc831ac1d341d744", "7d269cefeee5563354458df9512dfa94", "19dd9f96f63404aa16c2ec1b8e865786",
    "6c71b21cf8af494fb41602d8260882bf", "e768e81a4bcad148c8347c47a31d0bac", "5418d499019b50ba99d1d1fde58e7e60",
    "739626ee5ae3befca068444ec8320d14", "5c52a81158fb5476b597cb7dad2011ba", "66a038207da1dac957bfb9db9369982f",
    "0e4f3cfc67d586f9aeb15f7a3182ffbb", "6b2e2010e0e04d97a0166063712234b0", "229847442b636f153c7ebbb02a0474cf",
    "b0b3e4e3ab22ddcef631ab0c2504ca54", "9d59f9c2faf7007c68e84b7eaff3829b", "a96d3de33024bc0586e4fe3b84de4be5",
    "de91b6903ee8f9a634ce3ef60c55a5a7", "091f858be5084b42229779de6d118e2a", "f663438c85e04f66bed8df502e3d88db",
    "52cb9b65f53e3c4462d9feb6e38d7fc0", "8c6162f7646ecdebe556715d95bcabe2", "123291e4faf434aaf2c2dde21569fb88",
    "c7b7967d481fe9a18e95295c33e96ae8", "aa270cf5ba9afa7f3bc974532f04126e", "cdf8e350075019e3e28d1ac1097b2f67",
    "4191df6255084b083adf3c1bcb2d29e9", "3a95cd7166418d27c7d2f248dda86468", "ab151cf5837e67647c860963ac0c6597",
    "237e0e25940c45c14bbfd228796579a9", "960b3fc262777b51206352a617b4cb7a", "62d5b594b480ede962681043dd108b82",
    "c2d720b9d51113e97316b132b15dc68f", "9c4312dfdf427dd2dd12c0b7f6b901b1", "4f5d04529431371020c7264ea2a1db34",
    "2c908327915f79d2be60b662bd36ab39", "4ebf7b4ac757ad19872c58153be3c2f6", "25eedb7cb4711dccd2aab2afd674e209",
    "6f991d5747c03f51ef65155a47973ee8", "e78c9082e4002c7c9cf109e66c358a0d", "4bb08e31860024257c15acea374f0631",
    "587837d58345b3de57050872b31eabc8", "0394f6ad702d0c0b4162b7ea7f48b644", "7a7dbe438afa666be6688b780fc23375",
    "cdf0ab297bcd7904c5975fef6b7cf84c", "c0bf8f98f148cb090f085831c79c542c"
]

output_file = "quantconnect/gemini/batch_stats_raw.txt"

with open(output_file, "w") as f:
    for i, bid in enumerate(ids):
        f.write(f"--- IT {i+1} ({bid}) ---\n")
        f.flush()
        
        # Get General Stats
        res1 = subprocess.run(["python3", "api/poll_backtest.py", bid], capture_output=True, text=True)
        f.write(res1.stdout)
        
        # Get Yearly Stats
        res2 = subprocess.run(["python3", "api/get_yearly_stats.py", bid], capture_output=True, text=True)
        f.write(res2.stdout)
        f.write("\n")
        f.flush()
        print(f"Finished It {i+1}")
