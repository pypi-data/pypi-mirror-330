$source = @"
using System;
using System.IO;
using System.Diagnostics;
using System.ComponentModel;

public class PowershellRunner {
    static void Main(string[] args) {
        if(args.Length < 1) {
            Console.Error.WriteLine("Must supply at least one argument.");
            Environment.Exit(1);
        }
        string[] arguments = new string[args.Length - 1];
        Array.Copy(args, 1, arguments, 0, arguments.Length);
        string ps_arguments = string.Join(" ", arguments);
        try {
            Process p = new Process();
            p.StartInfo.UseShellExecute = false;
            p.StartInfo.RedirectStandardOutput = true;
            p.StartInfo.RedirectStandardError = true;
            p.StartInfo.FileName = "PowerShell.exe";
            p.StartInfo.Arguments = "-ExecutionPolicy ByPass -c & '" + Path.GetFullPath(args[0]) + "' " + ps_arguments;
            Console.WriteLine(p.StartInfo.Arguments);
            p.Start();

            string stdout = p.StandardOutput.ReadToEnd();
            string stderr = p.StandardError.ReadToEnd();

            p.WaitForExit();

            if(stdout != String.Empty) {
                Console.WriteLine(stdout);
            }
            if(stderr != String.Empty) {
                Console.Error.WriteLine(stderr);
            }
            Environment.Exit(p.ExitCode);
        } catch (Exception e) {
            Console.Error.WriteLine(e.Message);
            Environment.Exit(1);
        }
        Environment.Exit(1)
    }
}
"@

Add-Type -TypeDefinition $source -Language CSharp -OutputAssembly "powershell_wrapper.exe" -OutputType WindowsApplication
