using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Net.Sockets;
using System.Text;
using System.Windows.Forms;

namespace ProtectConexion
{
    public partial class frmEncrypterSIIAB : Form
    {
        public string flNM = string.Empty;
        public frmEncrypterSIIAB()
        {
        InitializeComponent();
    }

        private void btnCargaArch_Click(object sender, EventArgs e)
        {
            try
            {
                if (!File.Exists(@"C:\Windows\Microsoft.NET\Framework64\v4.0.30319\aspnet_regiis.exe"))
                {
                    MessageBox.Show("No existe \"ASPNET_REGIIS.EXE\", VERIFIQUE\rla documentación del sitio:\rhttp://requerimientos.i-vsp.com/projects\r/sae/wiki/Wiki",
                        "Error ASPNET_REGIIS", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    Application.Exit();
                    btnSalir.PerformClick();
                }


                if (rtxtbxCadenaActual.Text != "")
                {
                    rtxtbxCadenaActual.Text = "";
                    rtxtbxCadenaModificada.Text = "";
                }

                ofd.Filter = "config files (*.config)|*.config";
                ofd.FilterIndex = 2;
                ofd.RestoreDirectory = true;

                if (ofd.ShowDialog() == DialogResult.OK)
                {
                    flNM = Path.GetFileName(ofd.FileName);
                    if (flNM != "web.config")
                    {
                        // https://docs.microsoft.com/en-us/dotnet/api/system.io.path.getdirectoryname?view=netcore-3.1
                        txtPath.Text = Path.GetDirectoryName(ofd.FileName) + "\\web.config";
                        File.Move(ofd.FileName, Path.GetDirectoryName(ofd.FileName) + "\\web.config");
                    }
                    else
                    {
                        txtPath.Text = ofd.FileName;
                    }

                    if (txtPath.Text != null)
                    {
                        var fileStream = new FileStream(txtPath.Text, FileMode.Open, FileAccess.Read);
                        using (var streamReader = new StreamReader(fileStream, Encoding.UTF8))
                        {
                            rtxtbxCadenaActual.Text = streamReader.ReadToEnd();
                            fileStream.Close();
                            gpbxAccion.Enabled = true;
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("No se puede leer el archivo del disco. El error es: " + ex.Message, "Lectura del Archivo",
                    MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
        }

        private void btnSalir_Click(object sender, EventArgs e)
        {
            if (flNM == "app.config" && File.Exists(Path.GetDirectoryName(txtPath.Text) + "\\web.config"))
            {
                //txtPath.Text = Path.GetDirectoryName(txtPath.Text) + "\\app.config";
                File.Move(Path.GetDirectoryName(txtPath.Text) + "\\web.config", Path.GetDirectoryName(txtPath.Text) + "\\app.config");
            }
            //this.Close();
            Application.Exit();
        }

        private void btnEncripta_Click(object sender, EventArgs e)
        {
            try
            {
                ProtectRSA.Encr_CMD(Path.GetDirectoryName(txtPath.Text));
                var fileStream = new FileStream(txtPath.Text, FileMode.Open, FileAccess.Read);
                using (var streamReader = new StreamReader(fileStream, Encoding.UTF8))
                {
                    rtxtbxCadenaModificada.Text = streamReader.ReadToEnd();
                    fileStream.Close();
                }
                
                if (flNM=="app.config")
                {
                    txtPath.Text = Path.GetDirectoryName(txtPath.Text) + "\\app.config";
                    File.Move(Path.GetDirectoryName(txtPath.Text) + "\\web.config", Path.GetDirectoryName(txtPath.Text) + "\\app.config");
                }
                gpbxAccion.Enabled = false;
                btnEncripta.Enabled = false;
                rbCifra.Checked = false;
                btnCargaArch.Focus();
            }
            catch(Exception exp)
            {
                MessageBox.Show("Error al ingresa a la Clase CRIPT: " + exp.ToString(), "Encriptado", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
        }

        private void btnDencriptar_Click(object sender, EventArgs e)
        {
            try
            {
                ProtectRSA.Dencr_CMD(Path.GetDirectoryName(txtPath.Text));
                var fileStream = new FileStream(txtPath.Text, FileMode.Open, FileAccess.Read);
                using (var streamReader = new StreamReader(fileStream, Encoding.UTF8))
                {
                    rtxtbxCadenaModificada.Text = streamReader.ReadToEnd();
                    fileStream.Close();
                }

                if (flNM == "app.config")
                {
                    txtPath.Text = Path.GetDirectoryName(ofd.FileName) + "\\app.config";
                    File.Move(Path.GetDirectoryName(txtPath.Text) + "\\web.config", Path.GetDirectoryName(txtPath.Text) + "\\app.config");
                }
                gpbxAccion.Enabled = false;
                btnDencriptar.Enabled = false;
                rbDcifrar.Checked = false;
                btnCargaArch.Focus();
            }
            catch (Exception exp)
            {
                MessageBox.Show("Error al acceder a la Clase Decrip: " + exp.ToString(), "Error Decriptar", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
        }

        private void rbCifra_CheckedChanged(object sender, EventArgs e)
        {
            if (rbCifra.Checked)
            {
                btnEncripta.Enabled = true;
                btnDencriptar.Enabled = false;
            }
        }

        private void rbDcifra_CheckedChanged(object sender, EventArgs e)
        {
            if (rbDcifrar.Checked)
            {
                btnDencriptar.Enabled = true;
                btnEncripta.Enabled = false;
            }
        }

        private void frmProtectConnect_Load(object sender, EventArgs e)
        {

        }

        private void rbwebconfig_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void fileSystemWatcher1_Changed(object sender, System.IO.FileSystemEventArgs e)
        {

        }

        private void gbxPath_Enter(object sender, EventArgs e)
        {

        }

        private void gbxCadena_Enter(object sender, EventArgs e)
        {

        }

        private void gpbxAccion_Enter(object sender, EventArgs e)
        {

        }
    }
}