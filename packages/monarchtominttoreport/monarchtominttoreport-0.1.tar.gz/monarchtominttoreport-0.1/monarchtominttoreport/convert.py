import argparse
import sys
import polars as pl


def main() -> None:
    """
    Command line interface for MonarchToMintToReport utility
    """
    kwargs = {
        'description': 'Convert a Monarch transaction export CSV file to a Mint transaction log to open in MintToReport',
        'formatter_class': argparse.RawDescriptionHelpFormatter
    }
    parser = argparse.ArgumentParser(**kwargs)

    parser.add_argument('-i', '--input', type=str, required=True,
                        help='Path to a Monarch export transaction CSV file to read.')

    parser.add_argument('-o', '--output', type=str, required=False, default='monarchtomint-output.csv',
                        help='Path to write out the converted Mint-formatted transaction CSV file.')

    args = parser.parse_args()

    df = _convert(args.input)
    result = _output_mint_csv(df, args.output)
    
    return result



def _convert(input: str) -> pl.DataFrame:
    """Read a Monarch CSV transaction file and convert to Mint, return as a pl.DataFrame
    
    Parameters
    ----------
    :param input: path to a Monarch exported CSV transaction file
    :type input: str
    
    Returns
    -----------
    :return: A Polars DataFrame converted to Mint format
    :rtype: pl.DataFrame
    """
    try:
        df = pl.read_csv(input, try_parse_dates=True)
    except:
        print("Source CSV file was not able to be parsed properly.  Check that the file exists and is a valid CSV format.")
        sys.exit()
    print(df.head)
    
    df = df.with_columns(
        pl.col("Original Statement").alias("Original Description"),
        pl.col("Tags").str.replace(","," ").alias("Labels"),
        pl.col("Account").alias("Account Name"),
        pl.when(pl.col("Amount") > 0)
            .then(pl.lit("credit"))
            .otherwise(pl.lit("debit"))
            .alias("Transaction Type"),
        Description=pl.col("Merchant"),
        Amount=abs(pl.col("Amount"))
        
    ) 
    
    df = df.drop("Original Statement").drop("Merchant")
    
    
    print(df.head)
    #df.select([pl.col('Col3'), pl.col('Col2'), pl.col('Col1)])
    df_export=df.select([
        pl.col("Date"),
        pl.col("Description"),
        pl.col("Original Description"), 
        pl.col("Amount"), 
        pl.col("Transaction Type"),
        pl.col("Category"),
        pl.col("Account Name"), 
        pl.col("Labels"), 
        pl.col("Notes")  
    ])    
    
    return df_export


def _output_mint_csv(df: pl.DataFrame, output: str) -> bool:
    """Write out the dataframe in CSV format to the output path specified

    Parameters
    ----------
    :param df: The DataFrame to write
    :type df: pl.DataFrame 
    :param output: File path to write CSV out
    :type output: str
    
    Returns
    -----------
    :return: If the CSV file was written successfully or not
    :rtype: bool
    """
    
    df.write_csv(output, date_format=("%m/%d/%Y"))
    
    return True


if __name__ == '__main__':
    main()    