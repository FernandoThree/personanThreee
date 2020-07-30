namespace ProtectConexion
{
    partial class frmEncrypterSIIAB
    {
        /// <summary>
        /// Variable del diseñador necesaria.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Limpiar los recursos que se estén usando.
        /// </summary>
        /// <param name="disposing">true si los recursos administrados se deben desechar; false en caso contrario.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Código generado por el Diseñador de Windows Forms

        /// <summary>
        /// Método necesario para admitir el Diseñador. No se puede modificar
        /// el contenido de este método con el editor de código.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(frmEncrypterSIIAB));
            this.gbxCadena = new System.Windows.Forms.GroupBox();
            this.lblCadenaModificada = new System.Windows.Forms.Label();
            this.rtxtbxCadenaModificada = new System.Windows.Forms.RichTextBox();
            this.btnCargaArch = new System.Windows.Forms.Button();
            this.rtxtbxCadenaActual = new System.Windows.Forms.RichTextBox();
            this.lblCadenaActual = new System.Windows.Forms.Label();
            this.gbtnBotones = new System.Windows.Forms.GroupBox();
            this.btnSalir = new System.Windows.Forms.Button();
            this.btnDencriptar = new System.Windows.Forms.Button();
            this.btnEncripta = new System.Windows.Forms.Button();
            this.gbxPath = new System.Windows.Forms.GroupBox();
            this.txtPath = new System.Windows.Forms.TextBox();
            this.lblDirectorio = new System.Windows.Forms.Label();
            this.ofd = new System.Windows.Forms.OpenFileDialog();
            this.fbd = new System.Windows.Forms.FolderBrowserDialog();
            this.gpbxAccion = new System.Windows.Forms.GroupBox();
            this.rbDcifrar = new System.Windows.Forms.RadioButton();
            this.rbCifra = new System.Windows.Forms.RadioButton();
            this.gbxCadena.SuspendLayout();
            this.gbtnBotones.SuspendLayout();
            this.gbxPath.SuspendLayout();
            this.gpbxAccion.SuspendLayout();
            this.SuspendLayout();
            // 
            // gbxCadena
            // 
            this.gbxCadena.BackColor = System.Drawing.Color.DarkGray;
            this.gbxCadena.Controls.Add(this.lblCadenaModificada);
            this.gbxCadena.Controls.Add(this.rtxtbxCadenaModificada);
            this.gbxCadena.Controls.Add(this.btnCargaArch);
            this.gbxCadena.Controls.Add(this.rtxtbxCadenaActual);
            this.gbxCadena.Controls.Add(this.lblCadenaActual);
            this.gbxCadena.Location = new System.Drawing.Point(9, 10);
            this.gbxCadena.Name = "gbxCadena";
            this.gbxCadena.Size = new System.Drawing.Size(756, 294);
            this.gbxCadena.TabIndex = 0;
            this.gbxCadena.TabStop = false;
            this.gbxCadena.Text = "Cadena de conexión";
            this.gbxCadena.Enter += new System.EventHandler(this.gbxCadena_Enter);
            // 
            // lblCadenaModificada
            // 
            this.lblCadenaModificada.AutoSize = true;
            this.lblCadenaModificada.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblCadenaModificada.Location = new System.Drawing.Point(18, 161);
            this.lblCadenaModificada.Name = "lblCadenaModificada";
            this.lblCadenaModificada.Size = new System.Drawing.Size(194, 13);
            this.lblCadenaModificada.TabIndex = 4;
            this.lblCadenaModificada.Text = "Cadena de Conexión Modificada:";
            // 
            // rtxtbxCadenaModificada
            // 
            this.rtxtbxCadenaModificada.Location = new System.Drawing.Point(17, 181);
            this.rtxtbxCadenaModificada.Name = "rtxtbxCadenaModificada";
            this.rtxtbxCadenaModificada.Size = new System.Drawing.Size(626, 104);
            this.rtxtbxCadenaModificada.TabIndex = 3;
            this.rtxtbxCadenaModificada.Text = "";
            // 
            // btnCargaArch
            // 
            this.btnCargaArch.Location = new System.Drawing.Point(663, 94);
            this.btnCargaArch.Name = "btnCargaArch";
            this.btnCargaArch.Size = new System.Drawing.Size(75, 35);
            this.btnCargaArch.TabIndex = 2;
            this.btnCargaArch.Text = "Carga Archivo";
            this.btnCargaArch.UseVisualStyleBackColor = true;
            this.btnCargaArch.Click += new System.EventHandler(this.btnCargaArch_Click);
            // 
            // rtxtbxCadenaActual
            // 
            this.rtxtbxCadenaActual.Location = new System.Drawing.Point(17, 42);
            this.rtxtbxCadenaActual.Name = "rtxtbxCadenaActual";
            this.rtxtbxCadenaActual.Size = new System.Drawing.Size(626, 104);
            this.rtxtbxCadenaActual.TabIndex = 1;
            this.rtxtbxCadenaActual.Text = "";
            // 
            // lblCadenaActual
            // 
            this.lblCadenaActual.AutoSize = true;
            this.lblCadenaActual.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblCadenaActual.Location = new System.Drawing.Point(18, 23);
            this.lblCadenaActual.Name = "lblCadenaActual";
            this.lblCadenaActual.Size = new System.Drawing.Size(168, 13);
            this.lblCadenaActual.TabIndex = 0;
            this.lblCadenaActual.Text = "Cadena de Conexión Actual:";
            // 
            // gbtnBotones
            // 
            this.gbtnBotones.BackColor = System.Drawing.Color.DarkGray;
            this.gbtnBotones.Controls.Add(this.btnSalir);
            this.gbtnBotones.Controls.Add(this.btnDencriptar);
            this.gbtnBotones.Controls.Add(this.btnEncripta);
            this.gbtnBotones.Location = new System.Drawing.Point(148, 350);
            this.gbtnBotones.Name = "gbtnBotones";
            this.gbtnBotones.Size = new System.Drawing.Size(616, 89);
            this.gbtnBotones.TabIndex = 1;
            this.gbtnBotones.TabStop = false;
            // 
            // btnSalir
            // 
            this.btnSalir.Location = new System.Drawing.Point(270, 36);
            this.btnSalir.Name = "btnSalir";
            this.btnSalir.Size = new System.Drawing.Size(75, 23);
            this.btnSalir.TabIndex = 2;
            this.btnSalir.Text = "Salir";
            this.btnSalir.UseVisualStyleBackColor = true;
            this.btnSalir.Click += new System.EventHandler(this.btnSalir_Click);
            // 
            // btnDencriptar
            // 
            this.btnDencriptar.Enabled = false;
            this.btnDencriptar.Location = new System.Drawing.Point(149, 36);
            this.btnDencriptar.Name = "btnDencriptar";
            this.btnDencriptar.Size = new System.Drawing.Size(75, 23);
            this.btnDencriptar.TabIndex = 1;
            this.btnDencriptar.Text = "DesCifrar";
            this.btnDencriptar.UseVisualStyleBackColor = true;
            this.btnDencriptar.Click += new System.EventHandler(this.btnDencriptar_Click);
            // 
            // btnEncripta
            // 
            this.btnEncripta.Enabled = false;
            this.btnEncripta.Location = new System.Drawing.Point(25, 36);
            this.btnEncripta.Name = "btnEncripta";
            this.btnEncripta.Size = new System.Drawing.Size(75, 23);
            this.btnEncripta.TabIndex = 0;
            this.btnEncripta.Text = "Cifrar";
            this.btnEncripta.UseVisualStyleBackColor = true;
            this.btnEncripta.Click += new System.EventHandler(this.btnEncripta_Click);
            // 
            // gbxPath
            // 
            this.gbxPath.BackColor = System.Drawing.Color.DarkGray;
            this.gbxPath.Controls.Add(this.txtPath);
            this.gbxPath.Controls.Add(this.lblDirectorio);
            this.gbxPath.Location = new System.Drawing.Point(8, 307);
            this.gbxPath.Name = "gbxPath";
            this.gbxPath.Size = new System.Drawing.Size(756, 35);
            this.gbxPath.TabIndex = 2;
            this.gbxPath.TabStop = false;
            this.gbxPath.Enter += new System.EventHandler(this.gbxPath_Enter);
            // 
            // txtPath
            // 
            this.txtPath.Enabled = false;
            this.txtPath.Location = new System.Drawing.Point(75, 9);
            this.txtPath.Name = "txtPath";
            this.txtPath.Size = new System.Drawing.Size(463, 20);
            this.txtPath.TabIndex = 1;
            // 
            // lblDirectorio
            // 
            this.lblDirectorio.AutoSize = true;
            this.lblDirectorio.Location = new System.Drawing.Point(14, 12);
            this.lblDirectorio.Name = "lblDirectorio";
            this.lblDirectorio.Size = new System.Drawing.Size(55, 13);
            this.lblDirectorio.TabIndex = 0;
            this.lblDirectorio.Text = "Directorio:";
            // 
            // gpbxAccion
            // 
            this.gpbxAccion.BackColor = System.Drawing.Color.DarkGray;
            this.gpbxAccion.Controls.Add(this.rbDcifrar);
            this.gpbxAccion.Controls.Add(this.rbCifra);
            this.gpbxAccion.Enabled = false;
            this.gpbxAccion.Location = new System.Drawing.Point(8, 350);
            this.gpbxAccion.Name = "gpbxAccion";
            this.gpbxAccion.Size = new System.Drawing.Size(121, 89);
            this.gpbxAccion.TabIndex = 3;
            this.gpbxAccion.TabStop = false;
            // 
            // rbDcifrar
            // 
            this.rbDcifrar.AutoSize = true;
            this.rbDcifrar.Location = new System.Drawing.Point(22, 54);
            this.rbDcifrar.Name = "rbDcifrar";
            this.rbDcifrar.Size = new System.Drawing.Size(67, 17);
            this.rbDcifrar.TabIndex = 1;
            this.rbDcifrar.TabStop = true;
            this.rbDcifrar.Text = "Descifrar";
            this.rbDcifrar.UseVisualStyleBackColor = true;
            this.rbDcifrar.CheckedChanged += new System.EventHandler(this.rbDcifra_CheckedChanged);
            // 
            // rbCifra
            // 
            this.rbCifra.AutoSize = true;
            this.rbCifra.Location = new System.Drawing.Point(22, 19);
            this.rbCifra.Name = "rbCifra";
            this.rbCifra.Size = new System.Drawing.Size(49, 17);
            this.rbCifra.TabIndex = 0;
            this.rbCifra.TabStop = true;
            this.rbCifra.Text = "Cifrar";
            this.rbCifra.UseVisualStyleBackColor = true;
            this.rbCifra.CheckedChanged += new System.EventHandler(this.rbCifra_CheckedChanged);
            // 
            // frmEncrypterSIIAB
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.DarkGray;
            this.ClientSize = new System.Drawing.Size(777, 446);
            this.Controls.Add(this.gpbxAccion);
            this.Controls.Add(this.gbxPath);
            this.Controls.Add(this.gbtnBotones);
            this.Controls.Add(this.gbxCadena);
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Name = "frmEncrypterSIIAB";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "Encrypter SIIAB";
            this.Load += new System.EventHandler(this.frmProtectConnect_Load);
            this.gbxCadena.ResumeLayout(false);
            this.gbxCadena.PerformLayout();
            this.gbtnBotones.ResumeLayout(false);
            this.gbxPath.ResumeLayout(false);
            this.gbxPath.PerformLayout();
            this.gpbxAccion.ResumeLayout(false);
            this.gpbxAccion.PerformLayout();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.GroupBox gbxCadena;
        private System.Windows.Forms.Button btnCargaArch;
        private System.Windows.Forms.RichTextBox rtxtbxCadenaActual;
        private System.Windows.Forms.Label lblCadenaActual;
        private System.Windows.Forms.GroupBox gbtnBotones;
        private System.Windows.Forms.Button btnSalir;
        private System.Windows.Forms.Button btnDencriptar;
        private System.Windows.Forms.Button btnEncripta;
        private System.Windows.Forms.GroupBox gbxPath;
        private System.Windows.Forms.OpenFileDialog ofd;
        private System.Windows.Forms.TextBox txtPath;
        private System.Windows.Forms.Label lblDirectorio;
        private System.Windows.Forms.Label lblCadenaModificada;
        private System.Windows.Forms.RichTextBox rtxtbxCadenaModificada;
        private System.Windows.Forms.FolderBrowserDialog fbd;
        private System.Windows.Forms.GroupBox gpbxAccion;
        private System.Windows.Forms.RadioButton rbDcifrar;
        private System.Windows.Forms.RadioButton rbCifra;
    }
}

