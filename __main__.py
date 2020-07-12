import argparse
import bindwav

if __name__ == '__main__':
     
    parser = argparse.ArgumentParser()
    parser.add_argument(
            'head', type=str, help='e.g. \'ABC\' of \'ABC_01.wav\'')
    parser.add_argument(
            'n', type=int, help='number of channels')
    parser.add_argument(
            '--digit', type=int, default=0, help='number of digits (default:0)')
    parser.add_argument(
            '--chunk', type=int, default=2**14, help='chunk size (default:16384)')
     
    args = parser.parse_args()
    head = args.head
    N = args.n
    ndigits = args.digit
    chunksize = args.chunk

    try:
        bindwav.bind(head, N, ndigits, chunksize)
    except Exception as e:
        print(e)

