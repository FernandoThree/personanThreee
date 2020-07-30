using System;
using System.Configuration;
using System.Linq;
using System.Text;
using System.IO;
using System.Threading;
using System.Threading.Tasks;
using System.Linq.Expressions;
using System.Windows.Forms;
using System.Diagnostics;
using System.Web;

public class ProtectRSA
{
    public static void Encr_CMD(string pathFile)
    {
        try
        {
            ProcessStartInfo startInfo = new ProcessStartInfo("CMD.exe");
            startInfo.WindowStyle = ProcessWindowStyle.Hidden;    // Normal;
            startInfo.Arguments = "/c aspnet_regiis -pef \"connectionStrings\" \"" + pathFile + "\" -prov \"RsaProtectedConfigurationProvider\"";
            Process.Start(startInfo);
            Thread.Sleep(1500);
            startInfo.Arguments = "/c aspnet_regiis -pef \"appSettings\" \"" + pathFile + "\" -prov \"RsaProtectedConfigurationProvider\"";
            Process.Start(startInfo);
            Thread.Sleep(1500);
        }
        catch (Exception exp)
        {
            MessageBox.Show("Error al Encriptar el archivo: " + exp.ToString(), "Error al renombrar", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
    }

    public static void Dencr_CMD(string pathFile)
    {
        try
        {
            ProcessStartInfo startInfo = new ProcessStartInfo("CMD.exe");
            startInfo.WindowStyle = ProcessWindowStyle.Hidden;
            startInfo.Arguments = "/c aspnet_regiis -pdf \"connectionStrings\" \"" + pathFile + "\"";
            Process.Start(startInfo);
            Thread.Sleep(1500);
            startInfo.Arguments = "/c aspnet_regiis -pdf \"appSettings\" \"" + pathFile + "\"";
            Process.Start(startInfo);
            Thread.Sleep(1500);
        }
        catch (Exception exp)
        {
            MessageBox.Show("Error al Desencriptar el archivo: " + exp.ToString(), "Error al renombrar", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
    }
}