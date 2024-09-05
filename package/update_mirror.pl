#!/usr/bin/perl

use strict;
use warnings;
use autodie;

# my $mirrors = 'https://mirrors.tuna.tsinghua.edu.cn/centos-stream';
my $mirrors = 'https://mirrors.aliyun.com/centos-stream';
# my $mirrors = 'https://mirrors.aliyun.com/rockylinux';

if (@ARGV < 1) {
    die "Usage: $0 <filename1> <filename2> ...\n";
}

my $filename = "/etc/yum.repos.d/centos.repo";
my $keyword = "baseurl";
open(my $fh, '<', $filename) or die "Can not open '$filename' $!";
my $found = 0;
while (my $row = <$fh>) {
    chomp $row;
    if (index($row, $keyword) != -1) {
        $found = 1;
        last;
    }
}
close($fh);

if ($found) {  
        print "Find the keyword '$keyword' in '$filename'.\n";  
} else {
    while (my $filename = shift @ARGV) {
        my $backup_filename = $filename . '.bak';
        rename $filename, $backup_filename;
        open my $input, "<", $backup_filename;
        open my $output, ">", $filename;
        while (<$input>) {
            s/^metalink/# metalink/;
            if (m/^name/) {
                my (undef, $repo, $arch) = split /-/;
                $repo =~ s/^\s+|\s+$//g;
                ($arch = defined $arch ? lc($arch) : '') =~ s/^\s+|\s+$//g;

                if ($repo =~ /^Extras/) {
                    $_ .= "baseurl=${mirrors}/SIGs/\$releasever-stream/extras" . ($arch eq 'source' ? "/${arch}/" : "/\$basearch/") . "extras-common\n";
                } else {
                    $_ .= "baseurl=${mirrors}/\$releasever-stream/$repo" . ($arch eq 'source' ? "/" : "/\$basearch/") . ($arch ne '' ? "${arch}/tree/" : "os") . "\n";
                }
            }
            print $output $_;
        }
    }
}