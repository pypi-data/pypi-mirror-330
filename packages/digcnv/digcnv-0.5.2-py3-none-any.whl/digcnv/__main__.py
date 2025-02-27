from os.path import split, join
import pandas as pd
import sys
from sklearn import preprocessing

from digcnv import utils
from digcnv import CNVision
from digcnv import dataPreparation
from digcnv import dataVerif
from digcnv import digCnvModel
from digcnv.digCNV_logger import logger as dc_logger
from digcnv.digCNV_logger import changeLoggingLevel

def main():
    """Run DigCNV in one line script. 

    :raises Exception: _description_
    :return: Dataframe containing all CNVs with their describing features and the DigCNV prediction.
    :rtype: pd.Dataframe
    """    
    if len(sys.argv) < 2:
        raise Exception("You must give at least one argument: the pathway to the config file. Get example with the function ...")

    else:
        if len(sys.argv) == 3:
            v = sys.argv[2]
        else:
            v = False
        changeLoggingLevel(verbose=v)
        parameters = utils.readDigCNVConfFile(sys.argv[1])
        
        cnvs = CNVision.mergeMultipleCNVCallingOutputs([parameters["PC"],parameters["QS"]], ["PennCNV", "QuantiSNP"])
        dc_logger.info("CNVs dataframe shape = {}".format(cnvs.shape))
        
        cnvs = dataPreparation.addMicroArrayQualityData(cnvs, parameters["QC"])
        dc_logger.info("CNVs dataframe shape = {}".format(cnvs.shape))

        cnvs = dataPreparation.addDerivedFeatures(cnvs)
        dc_logger.info("CNVs dataframe shape = {}".format(cnvs.shape))

        cnvs = dataPreparation.addChromosomicAnnotation(cnvs, parameters["centromeres"], parameters["seg_dups"])
        dc_logger.info("CNVs dataframe shape = {}".format(cnvs.shape))    
   
        cnvs = dataPreparation.transformTwoAlgsFeatures(cnvs)
        dc_logger.info("CNVs dataframe shape = {}".format(cnvs.shape))

        model = digCnvModel.DigCnvModel()
        model.openPreTrainedDigCnvModel(parameters["DigCnvModel"])

    dataVerif.checkIfMandatoryColumnsExist(cnvs, post_data_preparation=True)
    dataVerif.checkColumnsformats(cnvs, post_data_preparation=False)
    cnvs, cnvs_with_na = dataVerif.computeNaPercentage(cnvs, dimensions=model._dimensions, remove_na_data=True)

    predicted_cnvs = model.predictCnvClasses(cnvs, use_percentage=parameters['output_prob'])
    cnvs_with_na["DigCNVpred"] = None
    predicted_cnvs = pd.concat([predicted_cnvs, cnvs_with_na])

    if parameters["save"]:
        predicted_cnvs.to_csv(parameters["output"], sep="\t")
        dc_logger.info("CNVs annotated and classified saved to = {}".format(parameters["output"]))    

if __name__ == "__main__":
    main()