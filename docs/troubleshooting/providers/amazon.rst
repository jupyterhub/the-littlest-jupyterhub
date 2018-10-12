=============================================
Troubleshooting issues on Amazon Web Services
=============================================

This is an incomplete list of issues people have run into when running
TLJH on Amazon Web Services (AWS), and how they have fixed them!

'Connection Refused' error after restarting server
==================================================

If you restarted your server from the EC2 Management Console & then try to access
your JupyterHub from a browser, you might get a **Connection Refused** error.
This is most likely because the **External IP** of your server has changed.

Check the **IPv4 Public IP** dislayed in the bottom of the `EC2 Management Console` 
screen for that instance matches the IP you are trying to access. If you have a 
domain name pointing to the IP address, you might have to change it to point to 
the new correct IP.

You can prevent public IP changes by `associating a static IP
<https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html>`_
with your server. In the Amazon Web Services ecosystem, the public static IP 
addresses are handled under `Elastic IP addresses` category of AWS; these 
addresses are tied to the overall AWS account. `This guide 
<https://dzone.com/articles/assign-fixed-ip-aws-ec2>`_ might be helpful. Notice 
there can be a cost to this. Although `the guide 
<https://dzone.com/articles/assign-fixed-ip-aws-ec2>`_ is outdated (generally 
half that `price now <https://aws.amazon.com/ec2/pricing/on-demand/#Elastic_IP_Addresses>`_), 
Amazon describes `here <https://aws.amazon.com/premiumsupport/knowledge-center/elastic-ip-charges/>`_ 
how the Elastic IP address feature is free when associated with a running 
instance, but that you'll be charged by the hour for maintaining that specific
IP address when it isn't associated with a running instance.
