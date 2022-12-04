#!/usr/bin/python3

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from tabulate import tabulate

PACKAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
DATA_DIR = os.path.join(PACKAGE_DIR, 'data')
BENCHMARK_DATA_DIR = os.path.join(DATA_DIR, 'benchmark_data')
BENCHMARK_DATA_PATH = os.path.join(BENCHMARK_DATA_DIR, 'data.csv')


def get_sec(time_str):
    """Get seconds from time."""
    m, s = time_str.split(':')
    return int(m) * 60 + float(s)

def expand_bytes(size_str):
    sizes = ['KB', 'MB', 'GB']
    for s in sizes:
        if s in size_str:
            s_int = int(size_str.replace(s, ''))
            if (s == 'KB'):
                s_int *= 10**3
            if (s == 'MB'):
                s_int *= 10**6
            if (s == 'GB'):
                s_int *= 10**9
    return s_int


def sanitize_data(dataframe):
    dataframe.columns = dataframe.columns.str.strip()
    dataframe['File_Name'] = dataframe['File_Name'].str.strip()
    dataframe['Compression_Algo'] = dataframe['Compression_Algo'].str.strip()
    dataframe['Input_File_Size'] = dataframe['File_Name'].apply(expand_bytes)
    dataframe['Wall_Clock_Time'] = dataframe['Wall_Clock_Time'].apply(get_sec)
    dataframe['Size_Delta'] = dataframe['Input_File_Size'] - dataframe['Encrypted_Size_(Bytes)']
    dataframe = dataframe.rename(columns={'Wall_Clock_Time': 'Wall_Clock_Time_(seconds)'})

    # average the duplicates (reruns)
    dataframe = dataframe.groupby(['Algorithm', 'File_Name', 'Compression_Algo']).mean().reset_index()

    dataframe = dataframe.astype({'Algorithm':str, 'File_Name':str, 'Compression_Algo':str, 
                                                        'Encrypted_Size_(Bytes)':int, 'Resident_Size':int, 'User_Time':float, 'System_Time':float,
                                                        'Wall_Clock_Time_(seconds)':float, 'Time_Nanoseconds':int, 'Input_File_Size':int,
                                                        'Size_Delta':int})

    sorted_dataframe = dataframe.sort_values(
                                    ['Algorithm', 'Input_File_Size', 'Compression_Algo'], 
                                    ascending=[True, True, True])
    sorted_cols = ['Algorithm', 'File_Name', 'Compression_Algo', 
                    'Input_File_Size', 'Encrypted_Size_(Bytes)', 'Size_Delta', 'Resident_Size',
                    'User_Time', 'System_Time', 'Wall_Clock_Time_(seconds)', 'Time_Nanoseconds']
    return sorted_dataframe[sorted_cols].reset_index(drop=True)


def plot_size_time(dataframe):
    no_compression_df = dataframe[dataframe['Compression_Algo'] == 'none']

    for encr_alg in no_compression_df['Algorithm'].unique():
        enc_alg_df_subset = no_compression_df[no_compression_df['Algorithm'] == encr_alg]
        plt.plot(enc_alg_df_subset['Input_File_Size'], enc_alg_df_subset['Time_Nanoseconds'], label=encr_alg)

    plt.title('Compression algorithm runtimes (without compression)')
    plt.xlabel('Input file size (bytes)')
    plt.ylabel('Time (nanoseconds)')
    plt.tight_layout()
    plt.legend()
    plt.show()
            
def plot_size_diff(dataframe):
    no_compression_df = dataframe[dataframe['Compression_Algo'] == 'none']

    for encr_alg in no_compression_df['Algorithm'].unique():
        enc_alg_df_subset = no_compression_df[no_compression_df['Algorithm'] == encr_alg]
        plt.plot(enc_alg_df_subset['Input_File_Size'], enc_alg_df_subset['Encrypted_Size_(Bytes)'], label=encr_alg)

    plt.title('Compression algorithm file size (without compression)')
    plt.xlabel('Input file size (bytes)')
    plt.ylabel('Encrypted Size (bytes)')
    plt.tight_layout()
    plt.legend()
    plt.show()


def plot_size_diff_bar(dataframe):
    for encr_alg in dataframe['Algorithm'].unique():
        enc_alg_df_subset = dataframe[dataframe['Algorithm'] == encr_alg]

        enc_alg_df_subset_cols = enc_alg_df_subset[['File_Name', 'Compression_Algo', 'Size_Delta']]
        bzip_subset = enc_alg_df_subset_cols[enc_alg_df_subset_cols['Compression_Algo'] == 'BZIP2']
        zip_subset = enc_alg_df_subset_cols[enc_alg_df_subset_cols['Compression_Algo'] == 'ZIP']
        zlib_subset = enc_alg_df_subset_cols[enc_alg_df_subset_cols['Compression_Algo'] == 'ZLIB']
        none_subset = enc_alg_df_subset_cols[enc_alg_df_subset_cols['Compression_Algo'] == 'none']

        x = np.arange(4)
        width = 0.2

        plt.bar(x-0.3, bzip_subset['Size_Delta'], width, label='BZIP')
        plt.bar(x-0.1, zip_subset['Size_Delta'], width, label='ZIP')
        plt.bar(x+0.1, zlib_subset['Size_Delta'], width, label='ZLIB')
        plt.bar(x+0.3, none_subset['Size_Delta'], width, label='None')

        plt.xticks(x, bzip_subset['File_Name'])
        plt.title('File size after ' + encr_alg + 'encryption and compression')
        plt.xlabel('Input file size (bytes)')
        plt.ylabel('Encrypted Size (bytes)')
        plt.tight_layout()
        plt.legend()
        plt.show()


def plot_size_diff_bar_pct(dataframe):
    for encr_alg in dataframe['Algorithm'].unique():
        enc_alg_df_subset = dataframe[dataframe['Algorithm'] == encr_alg]

        enc_alg_df_subset['Pct_Diff'] = enc_alg_df_subset['Size_Delta']/enc_alg_df_subset['Input_File_Size']*100
        enc_alg_df_subset['Pct_Diff'] = enc_alg_df_subset['Encrypted_Size_(Bytes)']/enc_alg_df_subset['Input_File_Size']*100
        enc_alg_df_subset_cols = enc_alg_df_subset[['File_Name', 'Compression_Algo', 'Pct_Diff']]
        bzip_subset = enc_alg_df_subset_cols[enc_alg_df_subset_cols['Compression_Algo'] == 'BZIP2']
        zip_subset = enc_alg_df_subset_cols[enc_alg_df_subset_cols['Compression_Algo'] == 'ZIP']
        zlib_subset = enc_alg_df_subset_cols[enc_alg_df_subset_cols['Compression_Algo'] == 'ZLIB']
        none_subset = enc_alg_df_subset_cols[enc_alg_df_subset_cols['Compression_Algo'] == 'none']

        x = np.arange(4)
        width = 0.2

        plt.bar(x-0.3, bzip_subset['Pct_Diff'], width, label='BZIP')
        plt.bar(x-0.1, zip_subset['Pct_Diff'], width, label='ZIP')
        plt.bar(x+0.1, zlib_subset['Pct_Diff'], width, label='ZLIB')
        plt.bar(x+0.3, none_subset['Pct_Diff'], width, label='None')
        print(bzip_subset['File_Name'])

        plt.xticks(x, bzip_subset['File_Name'])
        plt.title('File size after ' + encr_alg + ' encryption and compression')
        plt.xlabel('Input file size (bytes)')
        plt.ylabel('Encrypted size percent (relative to input)')
        plt.tight_layout()
        plt.legend()
        #plt.show()
        plt.savefig("./data/graphs/"+encr_alg + ".png")
        plt.cla()

if __name__ == "__main__":
    data_df = pd.read_csv(BENCHMARK_DATA_PATH)
    data_df = sanitize_data(data_df)
    #data_df.to_csv('formatted_data.csv')
    #print(tabulate(data_df, headers='keys'))
    #plot_size_time(data_df)
    #plot_size_diff(data_df)
    #plot_size_diff_bar(data_df)
    plot_size_diff_bar_pct(data_df)