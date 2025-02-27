# -*- coding: utf-8 -*-

import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
import PyQt5.QtWidgets as qtw

import pandas as pd

from xpcsutilities.tools.result_file import XPCSResultFile

import numpy as np
import logging, os
logger = logging.getLogger(__name__)



class XPCSExportDialog(qtw.QDialog):
    """
    Contain the export dialog
    """
    
    def __init__(self, files, parent=None):
        super().__init__(parent)
        
        self.__files = files
        
        self.setWindowTitle("Export to ASCII")
        
        self.__layout = qtw.QFormLayout()
        self.setLayout(self.__layout)
        
        self.__exportext = qtw.QLineEdit()
        self.__exportext.setText("_ascii.txt")
        self.__layout.addRow("Filename extension", self.__exportext)
        
        self.__exportheaders = qtw.QCheckBox()
        self.__exportheaders.setChecked(True)
        self.__layout.addRow("Add headers to data export", self.__exportheaders)
        
        self.__exportpath = qtw.QPushButton(os.getcwd())
        self.__exportpath.clicked.connect(self.changeExportDirectory)
        self.__layout.addRow("Export to", self.__exportpath)
        
        self.__exportFmt = qtw.QComboBox()
        self.__exportFmt.addItem("Pandas DataFrame")
        self.__exportFmt.addItem("Array, one column per q and direction")
        self.__exportFmt.addItem("Array, one column per q, one section by direction")
        self.__layout.addRow("Export format", self.__exportFmt)
        
        self.__eraseStrategy = qtw.QComboBox()
        self.__eraseStrategy.addItem("Do nothing")
        self.__eraseStrategy.addItem("Overwrite")
        self.__eraseStrategy.addItem("Save new file with suffix")
        self.__layout.addRow("If output file already exist", self.__eraseStrategy)
        
        self.__exportbtn = qtw.QPushButton("Export")
        self.__exportbtn.clicked.connect(self.export)
        self.__layout.addRow(self.__exportbtn)
        
        
    def changeExportDirectory(self):
        """
        Change the directory where the data are exported
        """
        
        newd = qtw.QFileDialog.getExistingDirectory(self, "Export data to ...", self.__exportpath.text())
        
        if os.path.isdir(newd):
            self.__exportpath.setText(newd)
            
    def export(self):
        """
        Export the data files to ASCII
        """
        extension = self.__exportext.text() 
        basepath = self.__exportpath.text()
        for f in self.__files:
            
            logger.info(f"Exporting {f}")
            
            basename = os.path.basename(f)
            
            if '.' in basename:
                basename = '.'.join(basename.split('.')[:-1])
            
            filename = f"{basepath}/{basename}{extension}"
            
            logger.debug(f"Filename: {filename}")
            
            # If already exist, check what user wants
            if os.path.isfile(filename):
                # Option 1: skip the file
                if self.__eraseStrategy.currentIndex() == 0:
                    logger.info(f"Skip file {f}: Output file already exists")
                    continue
                
                # Option 2: Overwrite
                elif self.__eraseStrategy.currentIndex() == 1:
                    logger.info(f"Will overwrite output file {filename}")
                
                # Option 3: Find a free filename with suffix
                elif self.__eraseStrategy.currentIndex() == 2:
                
                    i = 0
                    newf = f"{filename}.{i}"
                    
                    while os.path.isfile(newf):
                        i += 1
                        newf = f"{filename}.{i}"
                        
                    filename = newf
                    logger.info(f"Found an alternative output filename: {filename}")
               
                logger.debug(f"Filename after overwrite policy: {filename}")
            
            with XPCSResultFile(f) as data_file:
                # Data format
                if self.__exportFmt.currentIndex() == 0: # Pandas format
                    data = []
                
                    for k in data_file.analysis_keys:
                        tau, cf, std = data_file.get_correlations(k)
                        qq = data_file.get_q_values(k)
                        
                        for i, q in enumerate(qq):
                            
                            dr = {'dir':k,
                                  'q': q,
                                  'tau': tau.ravel(),
                                  'cf': cf[i,:].ravel() }
                            
                            if std is not None:
                                dr['std'] = std[i,:].ravel()
                            
                            data.append(pd.DataFrame(dr))
            
                    fdata = pd.concat(data, ignore_index=True)
                    
                    fdata.to_csv(filename, float_format="%.5e", index=False)
                    
                elif self.__exportFmt.currentIndex() == 1: # Column/dir format
                
                    datas = None
                    titles = None
                    
                    for k in data_file.analysis_keys:
                        tau, cf, std = data_file.get_correlations(k)
                        qq = data_file.get_q_values(k)
                        
                        if datas is None:
                            datas = [tau.ravel(), ]
                            titles = ["lag", ]
                        
                        for i, q in enumerate(qq):
                            if std is not None:
                                datas += [cf[i,:].ravel(), std[i,:].ravel(),]
                                titles += [f"cf_{q:.2e}_{k}", f"std_{q:.2e}_{k}",]
                            else:
                                datas += [cf[i,:].ravel(),]
                                titles += [f"cf_{q:.2e}_{k}",]
                                
                            
                    datas = np.array(datas).T
                    
                    datas[~np.isfinite(datas)] = -10.
                            
                    with open(filename, 'w') as fd:
                        fd.write("#"+",".join(titles)+'\n')
                        np.savetxt(fd, datas, '%.5e', ',')
                    
                elif self.__exportFmt.currentIndex() == 2: # Section/dir format
                
                    with open(filename, 'w') as fd:
                        for k in data_file.analysis_keys:
                            datas = None
                            titles = None
                            tau, cf, std = data_file.get_correlations(k)
                            qq = data_file.get_q_values(k)
                            
                            if datas is None:
                                datas = [tau.ravel(), ]
                                titles = ["lag", ]
                            
                            for i, q in enumerate(qq):
                                if std is not None:
                                    datas += [cf[i,:].ravel(), std[i,:].ravel(),]
                                    titles += [f"cf_{q:.2e}", f"std_{q:.2e}",]
                                else:
                                    datas += [cf[i,:].ravel(),]
                                    titles += [f"cf_{q:.2e}",]
                                
                            datas = np.array(datas).T
                    
                            datas[~np.isfinite(datas)] = -10.
                            
                            fd.write(f"# {k}\n")
                            fd.write("#"+",".join(titles)+'\n')
                            np.savetxt(fd, datas, '%.5e', ',')
                            fd.write('\n\n')
                        
        self.close()
                


