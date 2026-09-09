Set-StrictMode -Version Latest

if (-not ("ReverbCredentialStore" -as [type])) {
    Add-Type -TypeDefinition @"
using System;
using System.ComponentModel;
using System.Runtime.InteropServices;
using System.Text;

public static class ReverbCredentialStore {
    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Unicode)]
    private struct Credential {
        public UInt32 Flags;
        public UInt32 Type;
        public string TargetName;
        public string Comment;
        public System.Runtime.InteropServices.ComTypes.FILETIME LastWritten;
        public UInt32 CredentialBlobSize;
        public IntPtr CredentialBlob;
        public UInt32 Persist;
        public UInt32 AttributeCount;
        public IntPtr Attributes;
        public string TargetAlias;
        public string UserName;
    }

    [DllImport("advapi32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
    private static extern bool CredWrite(ref Credential credential, UInt32 flags);

    [DllImport("advapi32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
    private static extern bool CredRead(
        string target, UInt32 type, UInt32 flags, out IntPtr credential);

    [DllImport("advapi32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
    private static extern bool CredDelete(string target, UInt32 type, UInt32 flags);

    [DllImport("advapi32.dll")]
    private static extern void CredFree(IntPtr buffer);

    public static void Write(string target, string secret) {
        byte[] bytes = Encoding.UTF8.GetBytes(secret);
        IntPtr blob = Marshal.AllocHGlobal(bytes.Length);
        try {
            Marshal.Copy(bytes, 0, blob, bytes.Length);
            Credential credential = new Credential {
                Type = 1,
                TargetName = target,
                CredentialBlobSize = (UInt32)bytes.Length,
                CredentialBlob = blob,
                Persist = 2,
                UserName = "Paperclip"
            };
            if (!CredWrite(ref credential, 0))
                throw new Win32Exception(Marshal.GetLastWin32Error());
        } finally {
            for (int index = 0; index < bytes.Length; index++) bytes[index] = 0;
            Marshal.FreeHGlobal(blob);
        }
    }

    public static string Read(string target) {
        IntPtr pointer;
        if (!CredRead(target, 1, 0, out pointer))
            throw new Win32Exception(Marshal.GetLastWin32Error());
        try {
            Credential credential = (Credential)Marshal.PtrToStructure(
                pointer, typeof(Credential));
            byte[] bytes = new byte[credential.CredentialBlobSize];
            Marshal.Copy(credential.CredentialBlob, bytes, 0, bytes.Length);
            return Encoding.UTF8.GetString(bytes);
        } finally {
            CredFree(pointer);
        }
    }

    public static void Delete(string target) {
        if (!CredDelete(target, 1, 0)) {
            int error = Marshal.GetLastWin32Error();
            if (error != 1168) throw new Win32Exception(error);
        }
    }
}
"@
}

function Set-ReverbCredential {
    param([Parameter(Mandatory)][string]$Target, [Parameter(Mandatory)][string]$Payload)
    [ReverbCredentialStore]::Write($Target, $Payload)
}

function Get-ReverbCredential {
    param([Parameter(Mandatory)][string]$Target)
    return [ReverbCredentialStore]::Read($Target)
}

function Remove-ReverbCredential {
    param([Parameter(Mandatory)][string]$Target)
    [ReverbCredentialStore]::Delete($Target)
}
