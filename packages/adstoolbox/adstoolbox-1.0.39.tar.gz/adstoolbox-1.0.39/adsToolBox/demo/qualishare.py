# Import des librairies
import adsToolBox as ads
import smbclient
import polars as pl

# Création du logger
logger = ads.Logger(ads.Logger.INFO, "AdsLogger")

# Paramètres de connexion à la source
SMB_host = "10.0.6.100"
SMB_path = "/national$/DSI_input_output/Inputs/Qualishare/"
SMB_username = "AFT-IFTIM\svc.smb.onyx.20000"
SMB_password = "1K@s$Able"

# Paramètres de connexion à la cible
BDD_ods01_server = "10.10.0.222"
BDD_ods01_port = "1433"
BDD_ods01_user = "app_onyx_ods01"
BDD_ods01_password = "xpoca59100!!"
BDD_ods01_database = "onyx_ods01"

#BDD_driver = "pytds"

# Paramètres du connecteur source
srcFileName = "EXTRACTION_REC_QUALISHARE_IMPORT_AMMON.xlsx"
srcFilePathName = "//" + SMB_host + SMB_path + srcFileName

# Paramètres du connecteur cible
trgSchema = "nx_staging"
trgTable = "QS_reclamation"
trgActionQuery = f"""
DROP TABLE IF EXISTS [{trgSchema}].[{trgTable}];
CREATE TABLE [{trgSchema}].[{trgTable}] (
    [ID] VARCHAR(5),
    [SX_REF_RECLAMATION] VARCHAR(15),
    [DATE_RECLAMATION] DATE,
    [IMPORT_AMMON_NATURE] VARCHAR(50),
    [ENT_REF] VARCHAR(50),
    [Ref_Personne] VARCHAR(50),
    [IMPORT_AMMON_AUTEUR] VARCHAR(50),
    [RESPONSABLE_TRAITEMENT.] VARCHAR(50),
    [RESPONSABLE_TRAITEMENT:Mail] VARCHAR(50),
    [DATE_CREATION] DATE,
    [IMPORT_AMMON_PRIORITE] VARCHAR(50),
    [IMPORT_AMMON_ETAT_ACTIVITE] VARCHAR(20),
    [IMPORT_AMMON_TYPE] VARCHAR(20),
    [SX_Date_Traitement] DATE,
    [Lien_Modification.] VARCHAR(8000),
    [OBJET_RECLAMATION.] VARCHAR(8000),
    [DATE_DERNIERE_MODIF] DATE,
    [INACTIF] VARCHAR(3),
    [SX_Date_Inactivation] DATE,
    [Type d'élément] VARCHAR(8000),
    [Chemin d'accès] VARCHAR(8000));
"""

# Connexion source : Dossier partagé "//10.0.6.100/national$/DSI_input_output/Inputs/Qualishare/"
smbclient.register_session(SMB_host, username=SMB_username, password=SMB_password)

# Connexion cible : BDD MSSql "onyx_ods01"
trgConn = ads.dbMssql({"database": BDD_ods01_database
                    , "user": BDD_ods01_user
                    , "password": BDD_ods01_password
                    , "port": BDD_ods01_port
                    , "host": BDD_ods01_server}
                    , logger)
trgConn.connect()

# Connecteur source : fichier Excel
with smbclient.open_file(srcFilePathName, mode="rb") as srcFile:
    src = pl.read_excel(source = srcFile.read(), sheet_id = 1)

print(src.columns)
print(src.dtypes)

# Connecteur cible : table nx_staging.QS_reclamation
trg = {
    "name": f"{trgSchema}.{trgTable}",
    "db": trgConn,
    "schema": trgSchema,
    "table": trgTable,
    "cols": src.columns
}

# Déclaration du pipeline
pipe = ads.pipeline({
    "tableau": src,
    "db_destination": trg},
    logger)

# Action sur la cible : supprimer si elle existe et créer
trgConn.sqlExec(trgActionQuery)

# Exécution du pipeline
res = pipe.run()
print(res)